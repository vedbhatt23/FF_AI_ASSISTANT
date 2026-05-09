"""
Pydantic models for API request/response schemas.
"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


# ──────────────────────────────────────────────
# Request Models
# ──────────────────────────────────────────────

class ChatRequest(BaseModel):
    """Incoming chat message from the frontend."""
    message: str = Field(..., min_length=1, max_length=2000, description="User question")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for context")
    filters: Optional[dict[str, Any]] = Field(None, description="Optional filters (year, genre, etc.)")


class IngestRequest(BaseModel):
    """Request to trigger data ingestion."""
    force: bool = Field(False, description="Force re-ingestion even if data exists")


# ──────────────────────────────────────────────
# Response Models
# ──────────────────────────────────────────────

class ToolExecution(BaseModel):
    """Metadata about a single tool execution for explainability."""
    tool_name: str = Field(..., description="Name of the tool that was called")
    arguments: dict[str, Any] = Field(default_factory=dict, description="Arguments passed to the tool")
    result_summary: str = Field(..., description="Brief summary of the tool's output")
    source_type: str = Field(..., description="Type of data source: sql_database, vector_store, computed")
    execution_time_ms: float = Field(..., description="Time taken to execute in milliseconds")
    row_count: Optional[int] = Field(None, description="Number of data rows returned")


class ChartData(BaseModel):
    """Structured data for frontend chart rendering."""
    chart_type: str = Field(..., description="Chart type: bar, line, pie, area")
    title: str = Field(..., description="Chart title")
    data: list[dict[str, Any]] = Field(..., description="Chart data points")
    x_key: str = Field(..., description="Key for x-axis")
    y_keys: list[str] = Field(..., description="Keys for y-axis series")
    colors: Optional[list[str]] = Field(None, description="Optional color palette")


class ChatResponse(BaseModel):
    """Response from the AI assistant."""
    answer: str = Field(..., description="Synthesized answer from the AI")
    conversation_id: str = Field(..., description="Conversation identifier")
    sources: list[ToolExecution] = Field(default_factory=list, description="Tool execution trace")
    chart_data: Optional[ChartData] = Field(None, description="Structured chart data if applicable")
    timestamp: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat(),
        description="Response timestamp",
    )


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    sqlite_status: str
    sqlite_tables: dict[str, int]
    chromadb_status: str
    chromadb_documents: int
    openai_status: str
    version: str = "1.0.0"


class IngestResponse(BaseModel):
    """Response from data ingestion."""
    status: str
    tables_loaded: dict[str, int]
    documents_loaded: int
    message: str
