# Production RAG Knowledge Base API

A production-style FastAPI RAG knowledge base API using LangChain, vector search, document ingestion, source-grounded answers, Docker, pytest, and GitHub Actions CI.

## Features

- FastAPI backend
- LangChain-powered document retrieval
- Local deterministic embeddings for repeatable tests
- Chroma vector database
- Document ingestion endpoint
- Semantic search endpoint
- Source-grounded answer endpoint
- Pydantic request and response validation
- Swagger/OpenAPI documentation
- pytest test coverage
- Docker support
- GitHub Actions CI

## Tech Stack

- Python
- FastAPI
- LangChain
- ChromaDB
- Pydantic
- pytest
- Docker
- GitHub Actions
- Uvicorn

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/ingest` | Ingest documents into the vector database |
| POST | `/search` | Search the knowledge base |
| POST | `/ask` | Ask a source-grounded question |

## Getting Started

### 1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1