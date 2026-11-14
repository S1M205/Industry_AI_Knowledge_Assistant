from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Directory for persistent vector data
VECTOR_DIR = Path("data/vector_store")
VECTOR_DIR.mkdir(parents=True, exist_ok=True)

INDEX_PATH = VECTOR_DIR / "faiss.index"
CHUNKS_PATH = VECTOR_DIR / "chunks.npy"


index = None
stored_chunks = []


def load_vector_store():
    """
    Load the FAISS index and stored chunks from disk.
    """

    global index, stored_chunks

    if INDEX_PATH.exists() and CHUNKS_PATH.exists():
        index = faiss.read_index(str(INDEX_PATH))
        stored_chunks = np.load(
            CHUNKS_PATH,
            allow_pickle=True
        ).tolist()


def create_vector_store(chunks):
    """
    Add new document chunks to the persistent FAISS vector store.
    """

    global index, stored_chunks

    if not chunks:
        raise ValueError("No chunks available to create the vector store.")

    texts = [chunk["text"] for chunk in chunks]

    # Create normalized embeddings
    embeddings = model.encode(
        texts,
        normalize_embeddings=True
    )

    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )

    # Create a new index if it doesn't exist
    if index is None:
        index = faiss.IndexFlatIP(embeddings.shape[1])

    # Add embeddings and chunks
    index.add(embeddings)
    stored_chunks.extend(chunks)

    # Save index and metadata to disk
    faiss.write_index(index, str(INDEX_PATH))

    np.save(
        CHUNKS_PATH,
        np.array(stored_chunks, dtype=object)
    )

    return len(chunks)


def search_documents(query, k=3):
    """
    Search for the most relevant document chunks.
    """

    if index is None or not stored_chunks:
        return []

    k = min(k, len(stored_chunks))

    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    )

    query_embedding = np.asarray(
        query_embedding,
        dtype="float32"
    )

    _, indices = index.search(query_embedding, k)

    results = []

    for chunk_index in indices[0]:
        if chunk_index != -1:
            results.append(stored_chunks[chunk_index])

    return results