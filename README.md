# Semantic-Q-A-Based-Search-Engine-

A FastAPI-based backend that enables PDF upload, text parsing, embedding via Hugging Face, vector storage with Qdrant, and querying using Hugging Face LLMs.

## Features

- Upload and parse PDFs
- Chunk and embed text using HuggingFace models
- Store and query chunks in Qdrant vector DB
- Answer questions using Gemini
- Dockerized for easy deployment

---

## Requirements

- Python 3.9+
- Docker & Docker Compose
- Qdrant running locally or on a server
---

## Installation

```bash
git clone https://github.com/Hamzaswailem/Semantic-Q-A-Based-Search-Engine-API.git
cd Semantic-Q-A-Based-Search-Engine-API
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Setup Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=  openai key
model_name= hugging face model_name
openai_model = openai_model name
google_model = google_model name
OPENAI_API_KEY=your_openai_key
QDRANT_URL=http://localhost:6333
openai_model=gpt-3.5-turbo
TOKENIZERS_PARALLELISM=false
```

---

## Running the App

### Start Qdrant

```bash
docker run -p 6333:6333 qdrant/qdrant
```

### Run FastAPI

```bash
uvicorn app.api.documents:app --reload
```

Visit docs: http://127.0.0.1:8000/docs

---

## API Endpoints

### `/api/upload` – Upload PDFs  
POST with one or multiple PDFs

### `/api/query` – Ask a question  
POST with a question and top_k

---

## Docker Usage

### To load the Docker image

```bash
docker load -i semantic-search.tar
```



### Run Container

```bash
docker run -p 8000:8000 semantic-search-engine
```

---


## License

MIT License

![IMAGE 2025-05-04 21:30:06](https://github.com/user-attachments/assets/2efa4d8d-8f02-4f77-b9e8-51196f5b7143)
![IMAGE 2025-05-04 21:30:12](https://github.com/user-attachments/assets/76131080-e5eb-47fa-a7f2-7627abe86306)
