import numpy as np
from rag_exp import DbElement
from sentence_transformers import SentenceTransformer

def cvt_txt2vec(text: str, model: SentenceTransformer) -> np.ndarray:
    """
    Convert text to vector using sentence-transformers model
    """
    embedding = model.encode(text)
    return np.array(embedding)

def calc_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Calculate cosine similarity between two vectors
    """
    vec1 = np.squeeze(vec1)
    vec2 = np.squeeze(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

if __name__ == "__main__":
    TOP_K_PICK = 3

    knowledge1 = DbElement(text="orange is on the desk")
    knowledge2 = DbElement(text="taro ate apple yesterday")
    knowledge3 = DbElement(text="uv is recommended in this project")
    dummy_db = [knowledge1, knowledge2, knowledge3]

    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    for i in range(len(dummy_db)):
        dummy_db[i].vector = cvt_txt2vec(dummy_db[i].text, model)

    question = "where is the orange?"
    query = model.encode(question)

    top_k_tmp = []
    for db_element in dummy_db:
        similarity = calc_similarity(query, db_element.vector)
        top_k_tmp.append([db_element.text, similarity])
        print(f"Similarity between query and '{db_element.text}': {similarity}")
    print("-----------")
    print("calc top_k")
    
    top_k_tmp.sort(key=lambda x: x[1], reverse=True)
    for i in range(TOP_K_PICK):
        print(f"num{i+1} is: {top_k_tmp[i][0]}, {top_k_tmp[i][1]}")
