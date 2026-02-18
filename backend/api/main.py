"""AegisAI FastAPI gateway."""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routers import incidents, reports
from backend.core.observability.langsmith_config import configure_langsmith
from dotenv import load_dotenv

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_langsmith()
    # Seed Neo4j on first start
    try:
        from backend.core.graph_rag.neo4j_client import Neo4jClient
        Neo4jClient().seed_sample_data()
    except Exception as e:
        print(f"[Neo4j seed] {e}")
    yield


app = FastAPI(title="AegisAI — Disaster Intelligence Platform", version="1.0.0", lifespan=lifespan)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

app.include_router(incidents.router, prefix="/api/v1/incidents", tags=["incidents"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["reports"])


@app.get("/health")
def health():
    return {"status": "ok", "service": "aegis-ai"}
