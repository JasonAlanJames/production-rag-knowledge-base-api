from typing import List, Optional
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str


class IngestRequest(BaseModel):
    directory: Optional[str] = Field(
        default=None,
        description="Optional directory path containing .txt documents to ingest."
    )


class IngestResponse(BaseModel):
    indexed_documents: int
    indexed_chunks: int
    vectorstore_path: str


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=2)
    top_k: Optional[int] = Field(default=None, ge=1, le=10)


class SourceDocument(BaseModel):
    source: str
    chunk_id: Optional[str] = None
    content: str


class SearchResponse(BaseModel):
    query: str
    results: List[SourceDocument]


class AskRequest(BaseModel):
    question: str = Field(..., min_length=2)
    top_k: Optional[int] = Field(default=None, ge=1, le=10)


class AskResponse(BaseModel):
    question: str
    answer: str
    sources: List[SourceDocument]
    grounded: bool