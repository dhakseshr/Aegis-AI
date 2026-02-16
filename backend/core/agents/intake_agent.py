"""Agent 1: Incident Intake — classify disaster, extract location + urgency."""
import uuid
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langsmith import traceable
from backend.core.state import AegisState
from backend.core.kafka.producer import publish
import os, json

llm = ChatOpenAI(model=os.getenv("MODEL_NAME", "gpt-4o"), temperature=0)

PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are a disaster classification expert. Extract JSON with keys: disaster_type, location, urgency (low/medium/high/critical), summary, affected_population_estimate."),
    ("human", "{query}")
])

@traceable(name="intake_agent")
def intake_agent(state: AegisState) -> AegisState:
    reasoning = [
        "Received raw query",
        "Classifying disaster type via LLM",
        "Extracting location and urgency",
        "Building incident metadata",
    ]
    try:
        chain = PROMPT | llm
        result = chain.invoke({"query": state["query"]})
        data = json.loads(result.content)
    except Exception as e:
        data = {"disaster_type": "unknown", "location": "unknown", "urgency": "high", "summary": state["query"]}
        state["errors"].append(f"intake_agent: {e}")

    state["incident_id"] = state.get("incident_id") or str(uuid.uuid4())
    state["disaster_type"] = data.get("disaster_type")
    state["location"] = data.get("location")
    state["urgency"] = data.get("urgency", "high")
    state["incident_metadata"] = data
    state["reasoning_traces"]["intake_agent"] = reasoning
    state["current_agent"] = "research_agent"
    state["created_at"] = datetime.utcnow().isoformat()

    publish("incident-topic", state["incident_id"], data)
    state["kafka_published"].append("incident-topic")
    return state
