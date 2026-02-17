"""Qdrant vector store wrapper with Agentic RAG support."""
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import os, uuid

COLLECTIONS = ["disaster_reports", "emergency_guidelines", "historical_events", "shelters", "infrastructure"]
VECTOR_SIZE = 384


class QdrantStore:
    def __init__(self):
        self.client = QdrantClient(
            host=os.getenv("QDRANT_HOST", "localhost"),
            port=int(os.getenv("QDRANT_PORT", 6333))
        )
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
        self._init_collections()

    def _init_collections(self):
        existing = [c.name for c in self.client.get_collections().collections]
        for name in COLLECTIONS:
            if name not in existing:
                self.client.create_collection(
                    collection_name=name,
                    vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
                )

    def upsert(self, collection: str, text: str, metadata: Dict[str, Any]) -> str:
        doc_id = str(uuid.uuid4())
        vector = self.encoder.encode(text).tolist()
        self.client.upsert(collection_name=collection, points=[
            PointStruct(id=doc_id, vector=vector, payload={"text": text, **metadata})
        ])
        return doc_id

    def search(self, collection: str, query: str, top_k: int = 5, filter_: Dict = None) -> List[Dict]:
        vector = self.encoder.encode(query).tolist()
        results = self.client.search(
            collection_name=collection,
            query_vector=vector,
            limit=top_k,
            query_filter=Filter(must=[FieldCondition(key=k, match=MatchValue(value=v))
                                      for k, v in (filter_ or {}).items()]) if filter_ else None
        )
        return [{"score": r.score, **r.payload} for r in results]

    def delete_collection(self, collection: str):
        self.client.delete_collection(collection)
