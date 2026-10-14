import numpy as np
from sentence_transformers import SentenceTransformer


class Vectorizer:
    """
    Handles text-to-vector conversion and similarity calculations
    """
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
    
    def text_to_vector(self, text: str) -> np.ndarray:
        """
        Convert text to vector using sentence-transformers model
        """
        embedding = self.model.encode(text)
        return np.array(embedding)
    
    def calc_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two vectors
        """
        vec1 = np.squeeze(vec1)
        vec2 = np.squeeze(vec2)
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
