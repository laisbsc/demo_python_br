# 🔥 FastAPI AI Image Generator with Logfire Observability

> Demo project for Python Brasil 2025 - Understanding Observability with Logfire, OpenTelemetry, Logs, Spans & Traces

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![OpenTelemetry](https://img.shields.io/badge/OpenTelemetry-Instrumented-orange.svg)](https://opentelemetry.io/)
[![Pydantic Logfire](https://img.shields.io/badge/Pydantic-Logfire-purple.svg)](https://pydantic.dev/logfire)

A **fully instrumented** FastAPI application that generates AI images using OpenAI's DALL-E 3 API, demonstrating real-world observability patterns with OpenTelemetry and Pydantic Logfire.

---

## 🎯 What This Demo Shows

This project demonstrates the **difference between traditional logs and modern observability** through:

- **Logs** → Flat, timestamped events that are hard to correlate
- **Spans** → Structured units of work with start/end times and context
- **Traces** → Complete request flows showing how everything connects

**Key Learning:** See how observability turns "something broke" into "here's exactly why it broke" 🔍

---

## ✨ Features

- 🖼️ **AI Image Generation** - Create images from text prompts using DALL-E 3
- 📊 **Full-Stack Instrumentation** - FastAPI, OpenAI, and HTTPX fully traced
- 🔗 **Distributed Tracing** - Follow requests from browser → API → OpenAI → storage
- 📈 **Real-time Observability** - View logs, spans, and traces in Pydantic Logfire
- 🎨 **Web Interface** - Simple UI to generate and display images

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- OpenAI API key ([get one here](https://platform.openai.com/api-keys))
- Pydantic Logfire account ([sign up free](https://logfire.pydantic.dev/))

### Installation

1. **Clone the repository**
```bash
   git clone https://github.com/laisbsc/demo_python_br.git
   cd demo_python_br
```

2. **Create virtual environment and install dependencies**
```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv add 'logfire[fastapi,httpx,openai]'
```

3. **Set up environment variables**
```bash
   export OPENAI_API_KEY="your-openai-api-key"
```

4. **Run the application**
```bash
   fastapi run main.py
```

5. **Open your browser**
```
   http://localhost:8000
```

---

## 🏗️ Architecture
```
Browser Request
    ↓
FastAPI Endpoint (/generate)
    ↓
OpenAI DALL-E 3 API (generate image)
    ↓
HTTPX Client (download image)
    ↓
Local Storage (save as .jpg)
    ↓
Response with display URL
```

### Instrumented Components

- **FastAPI** - Automatic span creation for HTTP requests
- **OpenAI Client** - Traces all API calls with prompts & responses
- **HTTPX** - Tracks image downloads with headers & timing
- **Custom Spans** - Manual instrumentation for business logic

---

## 📊 Observability in Action

### Traditional Logs (Before)
```
[2025-10-25 14:32:01] INFO: Generating image
[2025-10-25 14:32:03] INFO: Image size: 245678 bytes
[2025-10-25 14:32:05] INFO: Image generated successfully
```
**Problem:** Can't see relationships, duration, or nested operations

### Modern Traces (After)
```
POST /generate [2.5s]
├─ Generating image [0.1s]
├─ openai.images.generate [1.8s]
│  └─ prompt: "sunset over mountains"
├─ httpx.get [0.5s]
│  ├─ url: https://oaidalleapiprodscus.blob...
│  └─ size: 245678 bytes
└─ Image generated successfully [0.1s]
   └─ path: a3f7c9d2.jpg
```
**Benefit:** Complete context, timing, and relationships visible at a glance

---

## 🔧 Key Code Patterns

### Observability Instrumentation
```python
import logfire

logfire.configure()

logfire.instrument_fastapi(app, capture_headers=True)  
logfire.instrument_openai(openai_client)
logfire.instrument_httpx(http_client, capture_headers=True)
```

### Manual Spans
```python
@app.post('/generate')
async def generate_image(prompt: str) -> GenerateResponse:
    with logfire.span('generate_image', prompt=prompt):
        logfire.info('Generating image', prompt_length=len(prompt))
        # ... business logic ...
        logfire.info('Image generated successfully', path=path)
```

---

## 📚 Learn More

This demo was created for the **Python Brasil 2025** talk:
**Observability in Python with Pydantic Logfire** by Laís Carvalho.

### Key Concepts Covered
- ✅ What is Observability vs Monitoring
- ✅ Logs vs Spans vs Traces
- ✅ Structured logging with context
- ✅ Distributed tracing across services
- ✅ Full-stack instrumentation patterns

### Resources
- [OpenTelemetry Python Docs](https://opentelemetry.io/docs/languages/python/)
- [Pydantic Logfire](https://pydantic.dev/logfire)
- [Talk Slides](https://pitch.com/v/talk_python_brasil_oct_25-6tbaig)

---

## 🤝 Contributing

Feedback is extremely welcomed in the shape of PRs. Get contributing!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/<name>`)
3. Commit your changes (`git commit -m 'Add feature'`)
4. Push to the branch (`git push origin feature/<name>`)
5. Open a Pull Request

---

## 👩‍💻 Author

**Laís Carvalho** ([@laisbsc](https://github.com/laisbsc))
> _Adapted from a talk given by **Samuel Colvin** ([@samuelcolvin](https://github.com/samuelcolvin)) at PyCon PT 2025._

 Developer Advocate @ Pydantic

- 🐦 X: [@lais_bsc](https://x.com/lais_bsc)
- 💼 LinkedIn: [laisbsc](https://linkedin.com/in/laisbsc)

---

<div align="center">

**⭐ Star this repo if you found it helpful!**

Made with ❤️ for the Python community

</div>
