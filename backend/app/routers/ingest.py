"""
Ingest router — /api/ingest endpoint.
"""
import csv, logging
from pathlib import Path
from fastapi import APIRouter
from app.config import get_settings
from app.database import init_db, execute_many, get_table_counts, execute_safe_query
from app.vector_store import add_documents, chunk_text, get_collection_count
from app.models import IngestResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["ingest"])


def _load_csvs():
    """Load all CSVs into SQLite."""
    settings = get_settings()
    csv_dir = Path(settings.CSV_DATA_DIR)
    init_db()

    csv_table_map = {
        "movies.csv": ("movies", ["movie_id","title","genre","release_date","budget","revenue","rating","director","language"]),
        "viewers.csv": ("viewers", ["viewer_id","name","age","gender","city","subscription_tier","signup_date"]),
        "watch_activity.csv": ("watch_activity", ["activity_id","viewer_id","movie_id","watch_date","watch_duration_mins","completed","device"]),
        "reviews.csv": ("reviews", ["review_id","viewer_id","movie_id","rating","review_text","review_date"]),
        "marketing_spend.csv": ("marketing_spend", ["campaign_id","movie_id","channel","spend_amount","impressions","clicks","start_date","end_date"]),
        "regional_performance.csv": ("regional_performance", ["region_id","movie_id","city","views","revenue","avg_rating","month"]),
    }

    for filename, (table, columns) in csv_table_map.items():
        filepath = csv_dir / filename
        if not filepath.exists():
            logger.warning(f"CSV not found: {filepath}")
            continue

        # Check if already loaded
        existing = execute_safe_query(f"SELECT COUNT(*) as c FROM {table}")
        if existing and existing[0]["c"] > 0:
            logger.info(f"Table {table} already has data, skipping")
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = []
            for row in reader:
                values = tuple(row.get(col, "") for col in columns)
                rows.append(values)

        if rows:
            placeholders = ",".join(["?"] * len(columns))
            sql = f"INSERT INTO {table} ({','.join(columns)}) VALUES ({placeholders})"
            execute_many(sql, rows)
            logger.info(f"Loaded {len(rows)} rows into {table}")


def _load_documents():
    """Load and chunk documents into ChromaDB."""
    settings = get_settings()
    doc_dir = Path(settings.DOCUMENTS_DIR)
    if not doc_dir.exists():
        logger.warning(f"Documents directory not found: {doc_dir}")
        return

    if get_collection_count() > 0:
        logger.info("ChromaDB collection already has data, skipping")
        return

    all_docs, all_metas, all_ids = [], [], []
    doc_count = 0

    for filepath in doc_dir.glob("*.md"):
        text = filepath.read_text(encoding="utf-8")
        chunks = chunk_text(text, chunk_size=500, overlap=100)
        for i, chunk in enumerate(chunks):
            all_docs.append(chunk)
            all_metas.append({"source": filepath.stem, "chunk_index": i, "total_chunks": len(chunks)})
            all_ids.append(f"{filepath.stem}_chunk_{i}")
        doc_count += 1
        logger.info(f"Chunked {filepath.name}: {len(chunks)} chunks")

    # Also handle .txt files
    for filepath in doc_dir.glob("*.txt"):
        text = filepath.read_text(encoding="utf-8")
        chunks = chunk_text(text, chunk_size=500, overlap=100)
        for i, chunk in enumerate(chunks):
            all_docs.append(chunk)
            all_metas.append({"source": filepath.stem, "chunk_index": i, "total_chunks": len(chunks)})
            all_ids.append(f"{filepath.stem}_chunk_{i}")
        doc_count += 1

    if all_docs:
        add_documents(all_docs, all_metas, all_ids)
        logger.info(f"Loaded {doc_count} documents ({len(all_docs)} chunks) into ChromaDB")


@router.post("/ingest", response_model=IngestResponse)
async def ingest(force: bool = False):
    """Load CSVs into SQLite and documents into ChromaDB."""
    logger.info(f"Ingestion started (force={force})")
    try:
        _load_csvs()
        _load_documents()
        counts = get_table_counts()
        doc_count = get_collection_count()
        return IngestResponse(
            status="success", tables_loaded=counts,
            documents_loaded=doc_count, message="Data ingestion complete",
        )
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        return IngestResponse(
            status="error", tables_loaded={}, documents_loaded=0,
            message=f"Ingestion failed: {str(e)}",
        )
