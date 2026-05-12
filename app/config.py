from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Production RAG Knowledge Base API"
    app_version: str = "1.0.0"
    vectorstore_dir: str = "./vectorstore"
    sample_docs_dir: str = "./data/sample_docs"
    chunk_size: int = 500
    chunk_overlap: int = 75
    top_k: int = 3

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()