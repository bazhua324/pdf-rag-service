# rag-service-demo

A minimal RAG (Retrieval-Augmented Generation) API that lets you ask questions about your PDF documents. Built with FastAPI, LangChain, ChromaDB, and Google Gemini.

## How it works

1. PDFs are loaded, split into chunks, and embedded into a local ChromaDB vector store.
2. On each `/ask` request the top-3 relevant chunks are retrieved and passed as context to Gemini, which generates a grounded answer.

## Setup

**Prerequisites:** Python 3.13+, [uv](https://docs.astral.sh/uv/), a Google AI API key.

```bash
uv sync
```

Create a `.env` file in the project root:

```
GOOGLE_API_KEY=your_key_here
```

## Ingest a PDF

```bash
uv run python ingest.py path/to/document.pdf
```

## Run the server

```bash
uv run uvicorn app:app --reload
```

## Run with Docker

```bash
docker build -t rag-service .
docker run -p 8000:8000 --env-file .env -v ./chroma_db:/app/chroma_db rag-service
```

## API

### `GET /health`

```json
{"status": "ok"}
```

### `POST /ask`

**Request**

```json
{"question": "What programming languages does the candidate know?"}
```

**Response**

```json
{
  "answer": "The candidate is proficient in Python, Java, and JavaScript...",
  "sources": [
    {"page": 1, "snippet": "...relevant excerpt..."}
  ]
}
```

## Configuration

| Variable | Default | Description |
|---|---|---|
| `GOOGLE_API_KEY` | — | Required. Google AI API key. |
| `CHROMA_DIR` | `./chroma_db` | Directory for the ChromaDB vector store. |
| `EMBEDDING_MODEL` | `gemini-embedding-2-preview` | Gemini embedding model. |
| `LLM_MODEL` | `gemini-2.5-flash-lite` | Gemini chat model. |
