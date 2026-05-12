from typing import List

from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.config import get_settings
from app.rag.embeddings import HashEmbeddings


def get_vectorstore() -> Chroma:
    settings = get_settings()

    return Chroma(
        collection_name="knowledge_base",
        embedding_function=HashEmbeddings(),
        persist_directory=settings.vectorstore_dir,
    )


def search_knowledge_base(query: str, top_k: int | None = None) -> List[Document]:
    settings = get_settings()
    k = top_k or settings.top_k

    vectorstore = get_vectorstore()
    return vectorstore.similarity_search(query, k=k)