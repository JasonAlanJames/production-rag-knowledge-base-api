from fastapi import FastAPI

from app.config import get_settings
from app.rag.answer_generator import generate_grounded_answer
from app.rag.ingest import ingest_documents
from app.rag.retriever import search_knowledge_base
from app.schemas import (
    AskRequest,
    AskResponse,
    HealthResponse,
    IngestRequest,
    IngestResponse,
    SearchRequest,
    SearchResponse,
    SourceDocument,
)


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "A production-style RAG knowledge base API using FastAPI, LangChain, "
        "vector search, document ingestion, source-grounded answers, Docker, "
        "pytest, and GitHub Actions CI."
    ),
)


def document_to_source(document) -> SourceDocument:
    return SourceDocument(
        source=document.metadata.get("source", "unknown"),
        chunk_id=document.metadata.get("chunk_id"),
        content=document.page_content,
    )


@app.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(
        status="ok",
        app_name=settings.app_name,
        version=settings.app_version,
    )


@app.post("/ingest", response_model=IngestResponse)
def ingest(request: IngestRequest):
    indexed_documents, indexed_chunks, vectorstore_path = ingest_documents(
        directory=request.directory
    )

    return IngestResponse(
        indexed_documents=indexed_documents,
        indexed_chunks=indexed_chunks,
        vectorstore_path=vectorstore_path,
    )


@app.post("/search", response_model=SearchResponse)
def search(request: SearchRequest):
    documents = search_knowledge_base(
        query=request.query,
        top_k=request.top_k,
    )

    return SearchResponse(
        query=request.query,
        results=[document_to_source(document) for document in documents],
    )


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    documents = search_knowledge_base(
        query=request.question,
        top_k=request.top_k,
    )

    answer, grounded = generate_grounded_answer(
        question=request.question,
        documents=documents,
    )

    return AskResponse(
        question=request.question,
        answer=answer,
        sources=[document_to_source(document) for document in documents],
        grounded=grounded,
    )