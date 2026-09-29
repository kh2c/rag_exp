import numpy as np
from rag_exp.dummy_embed_model import embedding_stub, str2seednum

class DbElement:
    """
    dummy dataclass for testing and mocking database vector storage
    """
    text: str
    vector: np.ndarray

    def __init__(self, text: str):
        self.text = text
        self.vector = embedding_stub(seed=str2seednum(text))

    def to_db_format(self) -> list[float]:
        return self.vector.tolist()
