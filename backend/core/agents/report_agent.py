"""Agent 8: Report Generation — final emergency intelligence report."""
import json, os
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langsmith import traceable
from backend.core.state import AegisState
from backend.core.kafka.producer import publish

llm = ChatOpenAI(model=os.getenv("MODEL_NAME", "gpt-4o"), temperature=0.1)

PROMPT = ChatPromptTemplate.from_messages([
    ("system", """Generate a structured emergency intelligence report as JSON with:
executive_summary (string), severity_level, affected_areas (list),
critical_infrastructure_at_risk (list), immediate_actions (list),
evacuation_recommendations (list), resource_deployment (list),
coordination_contacts (list), estimated_affected_population, confidence_score."""),
    ("human", "All context: {context}")
])

@traceable(name="report_agent")
def report_agent(state: AegisState) -> AegisState:
    reasoning = [
        "Consolidating all agent outputs",
        "Applying verified strategy",
        "Structuring executive summary",
        "Generating final actionable report",
    ]
    context = {
        "incident": state.get("incident_metadata"),
        "strategy": state.get("verification_result", {}).get("corrected_strategy") or state.get("strategy"),
        "resources": state.get("available_resources", [])[:5],
        "risks": state.get("infrastructure_risks", [])[:5],
    }
    try:
        result = (PROMPT | llm).invoke({"context": json.dumps(context)})
        report = json.loads(result.content)
    except Exception as e:
        report = {"executive_summary": state.get("query"), "error": str(e)}
        state["errors"].append(f"report_agent: {e}")

    report["generated_at"] = datetime.utcnow().isoformat()
    report["incident_id"] = state["incident_id"]
    state["final_report"] = report
    state["reasoning_traces"]["report_agent"] = reasoning
    state["current_agent"] = "done"

    publish("report-topic", state["incident_id"], report)
    state["kafka_published"].append("report-topic")
    return state
