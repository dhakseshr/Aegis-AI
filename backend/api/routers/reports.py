"""Report retrieval and document ingestion."""
from fastapi import APIRouter, UploadFile, File, Form
from backend.api.routers.incidents import _store
from backend.core.rag.embeddings import ingest_pdf, ingest_text

router = APIRouter()


@router.get("/{incident_id}")
def get_report(incident_id: str):
    item = _store.get(incident_id, {})
    state = item.get("state") or {}
    return state.get("final_report", {"error": "report not ready"})


@router.get("")
def list_reports():
    return [
        {"incident_id": k, "status": v["status"],
         "location": (v.get("state") or {}).get("location")}
        for k, v in _store.items()
    ]


@router.post("/ingest")
async def ingest_document(
    file: UploadFile = File(None),
    text: str = Form(None),
    collection: str = Form("disaster_reports"),
    source: str = Form("manual"),
):
    if file:
        content = await file.read()
        count = ingest_pdf(content, collection, {"source": source, "filename": file.filename})
        return {"chunks_ingested": count, "collection": collection}
    elif text:
        count = ingest_text(text, collection, {"source": source})
        return {"chunks_ingested": count, "collection": collection}
    return {"error": "provide file or text"}
