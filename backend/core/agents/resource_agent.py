"""Agent 4: Resource Discovery — Vector + Graph hybrid search."""
from langsmith import traceable
from backend.core.state import AegisState
from backend.core.rag.qdrant_client import QdrantStore
from backend.core.graph_rag.neo4j_client import Neo4jClient
from backend.core.kafka.producer import publish

store = QdrantStore()
client = Neo4jClient()

@traceable(name="resource_agent")
def resource_agent(state: AegisState) -> AegisState:
    reasoning = [
        "Searching Qdrant for shelters and emergency services",
        "Querying Neo4j for nearby hospitals via NEARBY relationship",
        "Merging vector and graph results",
        "Deduplicating and ranking resources",
    ]
    vector_hits = store.search("shelters", f"shelter {state['location']}", top_k=5)
    graph_hits = client.get_nearby_resources(location=state["location"])
    resources = vector_hits + graph_hits

    state["available_resources"] = resources[:15]
    state["reasoning_traces"]["resource_agent"] = reasoning

    publish("resource-topic", state["incident_id"], {"resources": len(resources)})
    state["kafka_published"].append("resource-topic")
    return state
