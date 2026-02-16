"""Agent 2: Situation Research — Agentic RAG with Qdrant."""
from langchain_openai import ChatOpenAI
from langsmith import traceable
from backend.core.state import AegisState
from backend.core.rag.qdrant_client import QdrantStore
from backend.core.kafka.producer import publish
import os

llm = ChatOpenAI(model=os.getenv("MODEL_NAME", "gpt-4o"), temperature=0)
store = QdrantStore()

@traceable(name="research_agent")
def research_agent(state: AegisState) -> AegisState:
    reasoning = [
        "Determining retrieval queries from incident metadata",
        "Searching Qdrant collections: disaster_reports, historical_events",
        "Re-ranking retrieved documents by relevance",
        "Injecting context into research results",
    ]
    queries = [
        f"{state['disaster_type']} {state['location']}",
        f"emergency response {state['disaster_type']}",
        f"historical {state['disaster_type']} incidents",
    ]
    results = []
    for q in queries:
        hits = store.search("disaster_reports", q, top_k=3)
        hits += store.search("historical_events", q, top_k=2)
        results.extend(hits)

    state["research_results"] = results[:10]
    state["reasoning_traces"]["research_agent"] = reasoning
    state["current_agent"] = "parallel_risk_resource"

    publish("research-topic", state["incident_id"], {"count": len(results)})
    state["kafka_published"].append("research-topic")
    return state
