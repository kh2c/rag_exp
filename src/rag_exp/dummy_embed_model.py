import numpy as np
from sentence_transformers import SentenceTransformer

# Global model instance
_model = None

def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    return _model

def str2seednum(text: str) -> int:
    """Keep for compatibility, though unused now"""
    return sum(ord(c) for c in text)

def embedding_stub(text: str) -> np.ndarray:
    """Generate embedding using sentence-transformers model"""
    model = _get_model()
    embedding = model.encode(text)
    return np.array(embedding)
