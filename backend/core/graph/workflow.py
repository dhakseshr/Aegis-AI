"""LangGraph workflow — 8-agent pipeline with parallel execution."""
from langgraph.graph import StateGraph, END
from backend.core.state import AegisState
from backend.core.agents.intake_agent import intake_agent
from backend.core.agents.research_agent import research_agent
from backend.core.agents.risk_agent import risk_agent
from backend.core.agents.resource_agent import resource_agent
from backend.core.agents.knowledge_graph_agent import knowledge_graph_agent
from backend.core.agents.strategy_agent import strategy_agent
from backend.core.agents.verification_agent import verification_agent
from backend.core.agents.report_agent import report_agent


def merge_parallel(state: AegisState) -> AegisState:
    """No-op merge node after parallel risk + resource agents."""
    return state


def build_workflow() -> StateGraph:
    graph = StateGraph(AegisState)

    graph.add_node("intake", intake_agent)
    graph.add_node("research", research_agent)
    graph.add_node("risk", risk_agent)
    graph.add_node("resource", resource_agent)
    graph.add_node("merge", merge_parallel)
    graph.add_node("knowledge_graph", knowledge_graph_agent)
    graph.add_node("strategy", strategy_agent)
    graph.add_node("verification", verification_agent)
    graph.add_node("report", report_agent)

    graph.set_entry_point("intake")
    graph.add_edge("intake", "research")

    # Parallel branch
    graph.add_edge("research", "risk")
    graph.add_edge("research", "resource")
    graph.add_edge("risk", "merge")
    graph.add_edge("resource", "merge")

    graph.add_edge("merge", "knowledge_graph")
    graph.add_edge("knowledge_graph", "strategy")
    graph.add_edge("strategy", "verification")
    graph.add_edge("verification", "report")
    graph.add_edge("report", END)

    return graph.compile()


workflow = build_workflow()


def run_workflow(query: str, incident_id: str = None) -> AegisState:
    import uuid
    initial: AegisState = {
        "incident_id": incident_id or str(uuid.uuid4()),
        "query": query,
        "disaster_type": None,
        "location": None,
        "urgency": None,
        "incident_metadata": None,
        "research_results": None,
        "infrastructure_risks": None,
        "available_resources": None,
        "graph_context": None,
        "strategy": None,
        "verification_result": None,
        "final_report": None,
        "reasoning_traces": {},
        "errors": [],
        "current_agent": "intake",
        "kafka_published": [],
        "created_at": "",
    }
    return workflow.invoke(initial)
