# dummy_embedder.py
import numpy as np
from langchain_core.embeddings import Embeddings

class DummyEmbeddings(Embeddings):
    def embed_documents(self, texts):
        return [np.random.rand(1536).tolist() for _ in texts]

    def embed_query(self, text):
        return np.random.rand(1536).tolist()
