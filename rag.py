import os
import json
import hashlib
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

EMBEDDING_MODEL = "text-embedding-3-small"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150
TOP_K = 4

INDEX_DIR = os.path.join("notes", "index")


def _index_path(code):
    return os.path.join(INDEX_DIR, f"{code}.json")


def _hash_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Split notes into overlapping chunks, preferring paragraph boundaries."""
    text = text.strip()
    if not text:
        return []

    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    current = ""

    for para in paragraphs:
        if current and len(current) + len(para) + 2 > chunk_size:
            chunks.append(current)
            current = ""

        if len(para) <= chunk_size:
            current = f"{current}\n\n{para}" if current else para
        else:
            # A single paragraph longer than chunk_size: hard-split with overlap.
            if current:
                chunks.append(current)
                current = ""
            start = 0
            while start < len(para):
                end = start + chunk_size
                chunks.append(para[start:end])
                start = end - overlap

    if current:
        chunks.append(current)

    return chunks


def embed_texts(texts):
    if not texts:
        return []
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    return [item.embedding for item in response.data]


def load_index(code):
    path = _index_path(code)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_index(code, index):
    os.makedirs(INDEX_DIR, exist_ok=True)
    with open(_index_path(code), "w", encoding="utf-8") as f:
        json.dump(index, f)


def ensure_index(code, notes_text):
    """Return the embedding index for a module's notes, (re)building it if stale."""
    notes_hash = _hash_text(notes_text)
    index = load_index(code)
    if index and index.get("hash") == notes_hash:
        return index

    chunks = chunk_text(notes_text)
    if not chunks:
        return None

    embeddings = embed_texts(chunks)
    index = {"hash": notes_hash, "chunks": chunks, "embeddings": embeddings}
    save_index(code, index)
    return index


def retrieve_relevant_chunks(code, notes_text, query, top_k=TOP_K):
    """Embed `query`, retrieve the top_k most similar note chunks by cosine similarity."""
    if not notes_text or not notes_text.strip() or not query or not query.strip():
        return []

    try:
        index = ensure_index(code, notes_text)
        if not index or not index["embeddings"]:
            return []
        query_embedding = embed_texts([query])[0]
    except Exception:
        # Embedding/index build failed (e.g. API error) - caller falls back to raw notes.
        return []

    chunk_embeddings = np.array(index["embeddings"], dtype=np.float32)
    query_vec = np.array(query_embedding, dtype=np.float32)

    chunk_norms = np.linalg.norm(chunk_embeddings, axis=1)
    query_norm = np.linalg.norm(query_vec)
    if query_norm == 0:
        return []

    similarities = (chunk_embeddings @ query_vec) / (chunk_norms * query_norm + 1e-8)
    ranked = np.argsort(similarities)[::-1][:top_k]
    return [index["chunks"][i] for i in ranked if similarities[i] > 0]
