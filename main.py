from contextlib import asynccontextmanager
from pathlib import Path
from uuid import uuid4

import logfire
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from httpx import AsyncClient
from openai import AsyncOpenAI
from pydantic import BaseModel, Field
from starlette.responses import FileResponse

logfire.configure(service_name='demo_python_brasil')
http_client: AsyncClient
openai_client = AsyncOpenAI()
logfire.instrument_openai(openai_client)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    global http_client, openai_client
    async with AsyncClient() as _http_client:
        http_client = _http_client
        logfire.instrument_httpx(http_client, capture_headers=True)
        yield


app = FastAPI(lifespan=lifespan)
logfire.instrument_fastapi(app, capture_headers=True)
this_dir = Path(__file__).parent
image_dir = Path(__file__).parent / 'images'
image_dir.mkdir(exist_ok=True)
app.mount('/static', StaticFiles(directory=image_dir), name='static')

@app.get('/')
@app.get('/display/{image:path}')
async def main() -> FileResponse:
    return FileResponse(this_dir / 'page.html')


class GenerateResponse(BaseModel):
    next_url: str = Field(serialization_alias='nextUrl')


@app.post('/generate')
async def generate_image(prompt: str) -> GenerateResponse:
    logfire.info(f'Generating image', prompt=prompt, prompt_lenght=len(prompt))

    with logfire.span('call_openai_api'):
        response = await openai_client.images.generate(prompt=prompt, model='dall-e-2')
        assert response.data, 'No image in response'
        image_url = response.data[0].url
        assert image_url, 'No image URL in response'

    with logfire.span('download_and_save_image'):
        http_response = await http_client.get(image_url)
        http_response.raise_for_status()
        path = f'{uuid4().hex}.jpg'
        (image_dir / path).write_bytes(http_response.content)
        image_size = len(http_response.content)
        logfire.info(f'Image size: {image_size} bytes')
        logfire.info('Image generated successfully', image_path=path, image_size=image_size)

    return GenerateResponse(next_url=f'/display/{path}')


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)
