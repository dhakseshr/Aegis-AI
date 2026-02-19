"""Risk microservice."""
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AegisAI Risk Service")

class Payload(BaseModel):
    incident_id: str
    data: dict

@app.post("/process")
async def process(payload: Payload):
    return {"incident_id": payload.incident_id, "service": "risk", "status": "ok"}

@app.get("/health")
def health():
    return {"service": "risk-service", "status": "ok"}
