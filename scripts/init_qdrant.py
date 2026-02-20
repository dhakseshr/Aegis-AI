"""Seed Qdrant with sample disaster documents."""
from backend.core.rag.qdrant_client import QdrantStore
from backend.core.rag.embeddings import ingest_text

store = QdrantStore()

docs = [
    ("disaster_reports", "2015 Chennai floods caused severe damage to 40% of the city infrastructure including roads and power lines.", {"year": 2015, "location": "Chennai"}),
    ("emergency_guidelines", "During flood events, evacuate low-lying areas first. Establish relief camps at elevated locations.", {"type": "guideline"}),
    ("historical_events", "Cyclone Vardah 2016 hit Chennai with wind speeds of 140 kmph damaging 10000 trees and cutting power.", {"year": 2016}),
    ("shelters", "Anna University Campus Shelter: Capacity 800, Contact 044-22357000, Location: Guindy, Chennai.", {"location": "Guindy"}),
    ("infrastructure", "Metrowater desalination plant, Nemmeli, critical for water supply to south Chennai. Flood-prone zone.", {"type": "water"}),
]

for collection, text, meta in docs:
    ingest_text(text, collection, meta)

print("Qdrant seeded.")
