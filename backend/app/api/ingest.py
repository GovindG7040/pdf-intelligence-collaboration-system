from fastapi import APIRouter

from app.services.ingest_service import IngestService

# =====================================================
# CREATE ROUTER
# =====================================================

router = APIRouter(
    prefix="/ingest",
    tags=["Knowledge Base"],
)

# =====================================================
# CREATE SERVICE OBJECT
# =====================================================

ingest_service = IngestService()

# =====================================================
# INGEST KNOWLEDGE BASE
# =====================================================

@router.post("/")
def ingest_knowledge_base():

    ingest_service.ingest()

    return {
        "message": "Knowledge Base ingested successfully."
    }