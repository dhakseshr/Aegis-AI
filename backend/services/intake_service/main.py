"""Intake microservice."""
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AegisAI Intake Service")

class Payload(BaseModel):
    incident_id: str
    data: dict

@app.post("/process")
async def process(payload: Payload):
    return {"incident_id": payload.incident_id, "service": "intake", "status": "ok"}

@app.get("/health")
def health():
    return {"service": "intake-service", "status": "ok"}
