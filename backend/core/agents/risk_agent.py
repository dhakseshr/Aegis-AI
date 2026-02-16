"""Agent 3: Infrastructure Risk — Neo4j graph traversal."""
from langsmith import traceable
from backend.core.state import AegisState
from backend.core.graph_rag.neo4j_client import Neo4jClient
from backend.core.kafka.producer import publish

client = Neo4jClient()

@traceable(name="risk_agent")
def risk_agent(state: AegisState) -> AegisState:
    reasoning = [
        "Connecting to Neo4j knowledge graph",
        "Querying infrastructure nodes near disaster location",
        "Traversing AFFECTS and DEPENDS_ON relationships",
        "Ranking infrastructure by criticality",
    ]
    risks = client.get_infrastructure_risks(
        location=state["location"],
        disaster_type=state["disaster_type"]
    )
    state["infrastructure_risks"] = risks
    state["reasoning_traces"]["risk_agent"] = reasoning

    publish("risk-topic", state["incident_id"], {"risks": len(risks)})
    state["kafka_published"].append("risk-topic")
    return state
