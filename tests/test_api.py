from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "ok"
    assert "Production RAG Knowledge Base API" in data["app_name"]


def test_ingest_endpoint():
    response = client.post("/ingest", json={})

    assert response.status_code == 200
    data = response.json()

    assert data["indexed_documents"] >= 1
    assert data["indexed_chunks"] >= 1
    assert "vectorstore" in data["vectorstore_path"]


def test_search_endpoint():
    client.post("/ingest", json={})

    response = client.post(
        "/search",
        json={"query": "What is a production RAG system?", "top_k": 2},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["query"] == "What is a production RAG system?"
    assert len(data["results"]) >= 1
    assert "source" in data["results"][0]
    assert "content" in data["results"][0]


def test_ask_endpoint():
    client.post("/ingest", json={})

    response = client.post(
        "/ask",
        json={"question": "What does a production RAG system do?", "top_k": 2},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["grounded"] is True
    assert "retrieved knowledge base content" in data["answer"]
    assert len(data["sources"]) >= 1