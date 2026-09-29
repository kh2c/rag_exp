import numpy as np

def str2seednum(text: str)->int:
    return sum(ord(c) for c in text)

def embedding_stub(seed: int):
    np.random.seed(seed)
    return np.random.rand(3)
