"""
Application configuration using Pydantic Settings.
Loads from environment variables and .env file.
"""

from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o"

    # Database
    DATABASE_PATH: str = str(Path(__file__).parent.parent / "data" / "db" / "insights.db")

    # ChromaDB
    CHROMA_PERSIST_DIR: str = str(Path(__file__).parent.parent / "data" / "chroma_db")
    CHROMA_COLLECTION_NAME: str = "internal_documents"

    # Data paths
    CSV_DATA_DIR: str = str(Path(__file__).parent.parent / "data" / "csv")
    DOCUMENTS_DIR: str = str(Path(__file__).parent.parent / "data" / "documents")

    # Security
    API_KEY: str = "dev-api-key-change-me"
    RATE_LIMIT_PER_MINUTE: int = 30

    # App
    APP_NAME: str = "Secure AI Insights Assistant"
    DEBUG: bool = False
    CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


@lru_cache()
def get_settings() -> Settings:
    """Cached settings singleton."""
    return Settings()
