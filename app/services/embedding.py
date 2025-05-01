from sentence_transformers import SentenceTransformer
from typing import List
import os
#keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
model_name = os.getenv("model_name")

class Embedder:
    
    model = SentenceTransformer(model_name)
    
    @staticmethod
    def embed(texts: List[str]) -> List[List[float]]:
        if not texts:
            raise ValueError("No texts provided for embedding")
        return Embedder.model.encode(texts).tolist()
    
    @staticmethod
    def embed_query(text: str) -> List[float]:
        return Embedder.model.encode(text).tolist()
    
    
    
