"""Agent 5: Knowledge Graph — GraphRAG combining Neo4j + Qdrant."""
from langsmith import traceable
from backend.core.state import AegisState
from backend.core.graph_rag.neo4j_client import Neo4jClient
from backend.core.graph_rag.graph_queries import GraphQueries

client = Neo4jClient()

@traceable(name="knowledge_graph_agent")
def knowledge_graph_agent(state: AegisState) -> AegisState:
    reasoning = [
        "Building entity graph for incident location",
        "Traversing multi-hop relationships (Location->Flood->Hospital)",
        "Extracting contextual paths for affected entities",
        "Merging graph context with vector retrieval",
    ]
    graph_paths = client.run_query(
        GraphQueries.FULL_CONTEXT,
        {"location": state["location"], "disaster": state["disaster_type"]}
    )
    affected_entities = client.run_query(
        GraphQueries.AFFECTED_ENTITIES,
        {"location": state["location"]}
    )
    state["graph_context"] = {
        "paths": graph_paths,
        "affected_entities": affected_entities,
        "location": state["location"],
    }
    state["reasoning_traces"]["knowledge_graph_agent"] = reasoning
    return state
