"""
Health check router — /api/health endpoint.
"""
import logging
from fastapi import APIRouter
from openai import OpenAI
from app.config import get_settings
from app.database import get_table_counts
from app.vector_store import get_collection_count
from app.models import HealthResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health():
    """System health check: SQLite, ChromaDB, OpenAI connectivity."""
    settings = get_settings()

    # SQLite
    try:
        counts = get_table_counts()
        sqlite_status = "connected"
    except Exception as e:
        counts = {}
        sqlite_status = f"error: {str(e)[:100]}"

    # ChromaDB
    try:
        doc_count = get_collection_count()
        chroma_status = "connected"
    except Exception as e:
        doc_count = 0
        chroma_status = f"error: {str(e)[:100]}"

    # OpenAI
    try:
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        client.models.list()
        openai_status = "connected"
    except Exception as e:
        openai_status = f"error: {str(e)[:100]}"

    overall = "healthy" if all(
        s == "connected" for s in [sqlite_status, chroma_status, openai_status]
    ) else "degraded"

    return HealthResponse(
        status=overall, sqlite_status=sqlite_status, sqlite_tables=counts,
        chromadb_status=chroma_status, chromadb_documents=doc_count,
        openai_status=openai_status,
    )
