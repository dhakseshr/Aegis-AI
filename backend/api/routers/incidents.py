"""Incident submission and streaming."""
import asyncio, json, uuid
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, BackgroundTasks
from pydantic import BaseModel
from backend.core.graph.workflow import run_workflow

router = APIRouter()
_store: dict = {}  # in-memory for demo; replace with Redis


class IncidentRequest(BaseModel):
    query: str


@router.post("")
async def create_incident(req: IncidentRequest, background_tasks: BackgroundTasks):
    incident_id = str(uuid.uuid4())
    _store[incident_id] = {"status": "processing", "state": None}
    background_tasks.add_task(_run, incident_id, req.query)
    return {"incident_id": incident_id, "status": "processing"}


async def _run(incident_id: str, query: str):
    try:
        state = await asyncio.to_thread(run_workflow, query, incident_id)
        _store[incident_id] = {"status": "done", "state": state}
    except Exception as e:
        _store[incident_id] = {"status": "error", "error": str(e)}


@router.get("/{incident_id}")
def get_incident(incident_id: str):
    return _store.get(incident_id, {"status": "not_found"})


@router.websocket("/{incident_id}/stream")
async def stream_incident(websocket: WebSocket, incident_id: str):
    await websocket.accept()
    try:
        while True:
            item = _store.get(incident_id, {})
            await websocket.send_text(json.dumps({
                "incident_id": incident_id,
                "status": item.get("status", "pending"),
                "current_agent": (item.get("state") or {}).get("current_agent"),
                "reasoning_traces": (item.get("state") or {}).get("reasoning_traces", {}),
            }))
            if item.get("status") in ("done", "error"):
                break
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        pass
