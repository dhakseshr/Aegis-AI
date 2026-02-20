"""Seed Neo4j with Chennai disaster scenario."""
from backend.core.graph_rag.neo4j_client import Neo4jClient
client = Neo4jClient()
client.seed_sample_data()
print("Neo4j seeded.")
client.close()
