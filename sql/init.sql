-- Enable pgvector extension for vector similarity search
CREATE EXTENSION IF NOT EXISTS vector;

-- Create vectors table with vector column (384 dimensions for MiniLM model)
CREATE TABLE IF NOT EXISTS vectors (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    vector VECTOR(384) NOT NULL
);

-- Create index for efficient similarity search
CREATE INDEX IF NOT EXISTS vectors_vector_idx ON vectors 
USING ivfflat (vector vector_cosine_ops)
WITH (lists = 100);
