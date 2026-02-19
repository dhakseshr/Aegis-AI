"""Resource microservice."""
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AegisAI Resource Service")

class Payload(BaseModel):
    incident_id: str
    data: dict

@app.post("/process")
async def process(payload: Payload):
    return {"incident_id": payload.incident_id, "service": "resource", "status": "ok"}

@app.get("/health")
def health():
    return {"service": "resource-service", "status": "ok"}
