"""
Chat router — /api/chat endpoint.
"""
import logging
from fastapi import APIRouter
from app.models import ChatRequest, ChatResponse
from app.orchestrator.agent import process_chat

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a user question through the AI orchestrator.
    Returns a synthesized answer with source/tool execution metadata.
    """
    logger.info(f"Chat request: {request.message[:100]}...")
    response = await process_chat(request)
    logger.info(f"Chat response: {len(response.sources)} tools used")
    return response
