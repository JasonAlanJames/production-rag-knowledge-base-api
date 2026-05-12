import hashlib
import math
from typing import List

from langchain_core.embeddings import Embeddings


class HashEmbeddings(Embeddings):
    """
    Deterministic local embedding model for portfolio/demo use.

    This avoids external API calls while still allowing LangChain vector search
    to work consistently in tests, Docker, and GitHub Actions.
    """

    def __init__(self, dimensions: int = 128):
        self.dimensions = dimensions

    def _embed(self, text: str) -> List[float]:
        vector = [0.0] * self.dimensions
        tokens = text.lower().split()

        for token in tokens:
            digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
            index = int(digest[:8], 16) % self.dimensions
            vector[index] += 1.0

        norm = math.sqrt(sum(value * value for value in vector))
        if norm == 0:
            return vector

        return [value / norm for value in vector]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> List[float]:
        return self._embed(text)