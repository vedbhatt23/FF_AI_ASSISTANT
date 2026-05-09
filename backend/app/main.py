"""
FastAPI application entry point.
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.security.middleware import SecurityMiddleware
from app.routers import chat, ingest, health
from app.database import init_db, get_table_counts, close_connection

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    logger.info("Starting Secure AI Insights Assistant...")
    settings = get_settings()

    # Initialize database
    init_db()
    counts = get_table_counts()
    total_rows = sum(counts.values())

    if total_rows == 0:
        logger.info("Database is empty — triggering auto-ingestion...")
        from app.routers.ingest import _load_csvs, _load_documents
        _load_csvs()
        _load_documents()
        logger.info("Auto-ingestion complete")
    else:
        logger.info(f"Database has {total_rows} total rows across {len(counts)} tables")

    logger.info("Application ready!")
    yield

    # Shutdown
    close_connection()
    logger.info("Application shutdown complete")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title=settings.APP_NAME,
        description="Secure AI-powered analytics assistant for entertainment business intelligence",
        version="1.0.0",
        lifespan=lifespan,
    )

    # CORS
    origins = [o.strip() for o in settings.CORS_ORIGINS.split(",")]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Security middleware
    app.add_middleware(SecurityMiddleware)

    # Routers
    app.include_router(health.router)
    app.include_router(chat.router)
    app.include_router(ingest.router)

    return app


app = create_app()
