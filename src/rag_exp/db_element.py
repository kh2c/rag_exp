import numpy as np
from sentence_transformers import SentenceTransformer

class DbElement:
    """
    dummy dataclass for testing and mocking database vector storage
    """
    text: str
    vector: np.ndarray

    def __init__(self, text: str):
        self.text = text
        self.vector = None  # Initialize with None

    def to_db_format(self) -> list[float]:
        return self.vector.tolist() if self.vector is not None else []
