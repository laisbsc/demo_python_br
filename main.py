from contextlib import asynccontextmanager
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from httpx import AsyncClient
from openai import AsyncOpenAI
from pydantic import BaseModel, Field
from starlette.responses import FileResponse

http_client: AsyncClient
openai_client = AsyncOpenAI()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    global http_client, openai_client
    async with AsyncClient() as _http_client:
        http_client = _http_client
        yield


app = FastAPI(lifespan=lifespan)

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

    response = await openai_client.images.generate(prompt=prompt, model='dall-e-3')
    assert response.data, 'No image in response'

    image_url = response.data[0].url
    assert image_url, 'No image URL in response'
    http_response = await http_client.get(image_url)
    http_response.raise_for_status()
    path = f'{uuid4().hex}.jpg'
    (image_dir / path).write_bytes(http_response.content)
    image_size = len(http_response.content)
    return GenerateResponse(next_url=f'/display/{path}')


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)
