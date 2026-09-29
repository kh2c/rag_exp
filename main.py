import numpy as np
from rag_exp import DbElement, embedding_stub, str2seednum
from rag_exp.config import *

def calc_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    calculate cosine similarity between two vectors
    """
    # 行列なら1次元にsqueeze, 1次元ならそのまま
    vec1 = np.squeeze(vec1)
    vec2 = np.squeeze(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

if __name__ == "__main__":
    TOP_K_PICK = 1

    if CONNECT_TO_API == False:
        knowledge1 = DbElement(text="orange is on the desk")
        knowledge2 = DbElement(text="using vscode is allowed")
        knowledge3 = DbElement(text="uv is recommended in this project")
        dummy_db = [knowledge1, knowledge2, knowledge3]

        question = "where is the orange?"
        query = embedding_stub(seed=str2seednum(question))

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

        print("hoge")
