from typing import TypedDict, Optional, List, Dict, Any
from datetime import datetime


class AegisState(TypedDict):
    incident_id: str
    query: str
    disaster_type: Optional[str]
    location: Optional[str]
    urgency: Optional[str]                  # low / medium / high / critical
    incident_metadata: Optional[Dict[str, Any]]
    research_results: Optional[List[Dict]]
    infrastructure_risks: Optional[List[Dict]]
    available_resources: Optional[List[Dict]]
    graph_context: Optional[Dict[str, Any]]
    strategy: Optional[Dict[str, Any]]
    verification_result: Optional[Dict[str, Any]]
    final_report: Optional[Dict[str, Any]]
    reasoning_traces: Dict[str, List[str]]  # agent_name -> steps
    errors: List[str]
    current_agent: str
    kafka_published: List[str]
    created_at: str
