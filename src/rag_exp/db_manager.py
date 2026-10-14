import os
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Tuple
import numpy as np
from rag_exp.db_element import DbElement
from rag_exp.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


class DBManager:
    """
    Manages database operations for vector storage and retrieval using PostgreSQL
    """
    
    def __init__(self, db_path: str = None):
        """
        Initialize DB connection.
        db_path is kept for compatibility but not used with PostgreSQL.
        """
        self.conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
    
    def _ensure_vector_extension(self) -> None:
        """Ensure pgvector extension is available"""
        cursor = self.conn.cursor()
        cursor.execute("CREATE EXTENSION IF NOT EXISTS vector")
        self.conn.commit()
        cursor.close()
    
    def _ensure_table_exists(self) -> None:
        """Create vectors table if not exists"""
        self._ensure_vector_extension()
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vectors (
                id SERIAL PRIMARY KEY,
                text TEXT NOT NULL,
                vector VECTOR(384) NOT NULL
            )
        """)
        self.conn.commit()
        cursor.close()
    
    def _save_db(self) -> None:
        """DB connection is persistent, no need to save separately"""
        pass
    
    def add_vector(self, text: str, vector: np.ndarray) -> DbElement:
        """Add a new vector to the database"""
        self._ensure_table_exists()
        cursor = self.conn.cursor()
        vector_list = vector.tolist()
        cursor.execute(
            "INSERT INTO vectors (text, vector) VALUES (%s, %s) RETURNING id, text",
            (text, vector_list)
        )
        result = cursor.fetchone()
        self.conn.commit()
        cursor.close()
        return DbElement(text=result[1], vector=vector)
    
    def get_all(self) -> List[DbElement]:
        """Get all elements from the database"""
        self._ensure_table_exists()
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT text, vector::float[] FROM vectors")
        rows = cursor.fetchall()
        cursor.close()
        return [DbElement(text=r["text"], vector=np.array(r["vector"])) for r in rows]
    
    def search_top_k(self, query_vector: np.ndarray, k: int = 3) -> List[Tuple[str, float]]:
        """
        Search for top K similar vectors in the database.
        Returns list of (text, distance) tuples (lower distance = more similar).
        """
        self._ensure_table_exists()
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        # Use pgvector's <-> operator for vector similarity search
        cursor.execute(
            """
            SELECT text, vector <-> %s::float[] as distance 
            FROM vectors 
            ORDER BY distance 
            LIMIT %s
            """,
            (query_vector.tolist(), k)
        )
        rows = cursor.fetchall()
        cursor.close()
        # Convert distance to similarity score (1 / (1 + distance))
        results = []
        for r in rows:
            distance = float(r["distance"])
            similarity = 1.0 / (1.0 + distance)
            results.append((r["text"], similarity))
        return results
    
    def _calc_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Fallback: Calculate cosine similarity between two vectors"""
        vec1 = np.squeeze(vec1)
        vec2 = np.squeeze(vec2)
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    
    def clear(self) -> None:
        """Clear all entries from the database"""
        self._ensure_table_exists()
        cursor = self.conn.cursor()
        cursor.execute("TRUNCATE TABLE vectors RESTART IDENTITY")
        self.conn.commit()
        cursor.close()
    
    def close(self) -> None:
        """Close the database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None
