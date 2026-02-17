"""Document ingestion pipeline: PDF/image -> chunks -> embeddings -> Qdrant."""
import io, os
from typing import List, Dict
from sentence_transformers import SentenceTransformer
from backend.core.rag.qdrant_client import QdrantStore
import PyPDF2
from PIL import Image

store = QdrantStore()


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunks.append(" ".join(words[i: i + chunk_size]))
    return chunks


def ingest_pdf(file_bytes: bytes, collection: str, metadata: Dict) -> int:
    reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    text = " ".join(p.extract_text() or "" for p in reader.pages)
    chunks = chunk_text(text)
    for i, chunk in enumerate(chunks):
        store.upsert(collection, chunk, {**metadata, "chunk_index": i})
    return len(chunks)


def ingest_text(text: str, collection: str, metadata: Dict) -> int:
    chunks = chunk_text(text)
    for i, chunk in enumerate(chunks):
        store.upsert(collection, chunk, {**metadata, "chunk_index": i})
    return len(chunks)


def ingest_image_caption(caption: str, collection: str, metadata: Dict) -> str:
    return store.upsert(collection, caption, metadata)
