from pathlib import Path
from typing import List, Tuple

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import get_settings
from app.rag.embeddings import HashEmbeddings


def load_text_documents(directory: str) -> List[Document]:
    docs_path = Path(directory)

    if not docs_path.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")

    documents: List[Document] = []

    for file_path in docs_path.glob("*.txt"):
        content = file_path.read_text(encoding="utf-8").strip()

        if content:
            documents.append(
                Document(
                    page_content=content,
                    metadata={"source": str(file_path)}
                )
            )

    return documents


def split_documents(documents: List[Document]) -> List[Document]:
    settings = get_settings()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )

    chunks = splitter.split_documents(documents)

    for index, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = f"chunk-{index + 1}"

    return chunks


def ingest_documents(directory: str | None = None) -> Tuple[int, int, str]:
    settings = get_settings()
    docs_dir = directory or settings.sample_docs_dir

    documents = load_text_documents(docs_dir)
    chunks = split_documents(documents)

    vectorstore = Chroma(
        collection_name="knowledge_base",
        embedding_function=HashEmbeddings(),
        persist_directory=settings.vectorstore_dir,
    )

    if chunks:
        vectorstore.add_documents(chunks)

    return len(documents), len(chunks), settings.vectorstore_dir