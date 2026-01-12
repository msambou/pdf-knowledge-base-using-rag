import faiss
import numpy as np
from typing import List


class VectorStore:
    def __init__(self, dim: int):
        self.dim = dim
        self.index = faiss.IndexFlatIP(dim)  # cosine similarity
        self.texts: List[str] = []
        self.metadatas: List[dict] = []

    def add(
        self,
        embeddings: np.ndarray,
        texts: List[str],
        metadatas: List[dict],
    ):
        if embeddings.shape[1] != self.dim:
            raise ValueError("Embedding dimension mismatch")

        self.index.add(embeddings)
        self.texts.extend(texts)
        self.metadatas.extend(metadatas)

    def search(self, query_embedding: np.ndarray, k: int = 5):
        scores, indices = self.index.search(query_embedding, k)

        results = []
        for idx in indices[0]:
            if idx == -1:
                continue
            results.append({
                "text": self.texts[idx],
                "metadata": self.metadatas[idx],
            })

        return results
