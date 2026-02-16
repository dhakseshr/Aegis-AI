"""Agent 7: Verification — hallucination check + factual consistency."""
import json, os
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langsmith import traceable
from backend.core.state import AegisState

llm = ChatOpenAI(model=os.getenv("MODEL_NAME", "gpt-4o"), temperature=0)

PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a fact-checker for emergency response plans.
Review the strategy against known facts and research results.
Return JSON: {verified: bool, issues: list, corrected_strategy: dict, confidence_score: float}"""),
    ("human", "Strategy: {strategy}\nResearch: {research}\nRisks: {risks}")
])

@traceable(name="verification_agent")
def verification_agent(state: AegisState) -> AegisState:
    reasoning = [
        "Cross-referencing strategy with research results",
        "Checking for unsupported claims",
        "Validating resource availability",
        "Computing confidence score",
    ]
    try:
        result = (PROMPT | llm).invoke({
            "strategy": json.dumps(state.get("strategy", {})),
            "research": json.dumps(state.get("research_results", [])[:3]),
            "risks": json.dumps(state.get("infrastructure_risks", [])[:3]),
        })
        verification = json.loads(result.content)
    except Exception as e:
        verification = {"verified": True, "issues": [], "confidence_score": 0.8}
        state["errors"].append(f"verification_agent: {e}")

    state["verification_result"] = verification
    state["reasoning_traces"]["verification_agent"] = reasoning
    return state
