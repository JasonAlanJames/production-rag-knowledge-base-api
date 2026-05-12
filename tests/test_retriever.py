from app.rag.ingest import ingest_documents
from app.rag.retriever import search_knowledge_base


def test_retriever_returns_documents():
    ingest_documents()

    results = search_knowledge_base(
        query="AI workflow automation",
        top_k=2,
    )

    assert len(results) >= 1
    assert results[0].page_content
    assert "source" in results[0].metadata