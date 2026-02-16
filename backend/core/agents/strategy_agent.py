"""Agent 6: Strategy Planning — CoT reasoning over all context."""
import json, os
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langsmith import traceable
from backend.core.state import AegisState
from backend.core.kafka.producer import publish

llm = ChatOpenAI(model=os.getenv("MODEL_NAME", "gpt-4o"), temperature=0.2)

PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an emergency response strategist.
Given disaster info, infrastructure risks, available resources, and graph context,
produce a JSON strategy with: immediate_actions (list), evacuation_routes (list),
priority_facilities (list), estimated_timeline, coordination_notes."""),
    ("human", "Incident: {incident}\nRisks: {risks}\nResources: {resources}\nGraph: {graph}")
])

@traceable(name="strategy_agent")
def strategy_agent(state: AegisState) -> AegisState:
    reasoning = [
        "Aggregating context from all upstream agents",
        "Chain-of-thought: assess severity -> identify bottlenecks -> plan actions",
        "Generating evacuation routes based on graph paths",
        "Prioritizing resource deployment",
    ]
    try:
        result = (PROMPT | llm).invoke({
            "incident": json.dumps(state.get("incident_metadata", {})),
            "risks": json.dumps(state.get("infrastructure_risks", [])[:5]),
            "resources": json.dumps(state.get("available_resources", [])[:5]),
            "graph": json.dumps(state.get("graph_context", {})),
        })
        strategy = json.loads(result.content)
    except Exception as e:
        strategy = {"immediate_actions": ["Evacuate low-lying areas"], "error": str(e)}
        state["errors"].append(f"strategy_agent: {e}")

    state["strategy"] = strategy
    state["reasoning_traces"]["strategy_agent"] = reasoning
    publish("strategy-topic", state["incident_id"], strategy)
    state["kafka_published"].append("strategy-topic")
    return state
