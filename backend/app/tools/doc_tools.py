"""
Document search tools for unstructured data queries via ChromaDB.
"""

import logging
from typing import Any, Optional

from app.vector_store import search_documents

logger = logging.getLogger(__name__)


def search_internal_documents(
    query: str,
    n_results: int = 5,
) -> list[dict[str, Any]]:
    """
    Search internal company documents using semantic similarity.

    Args:
        query: Natural language search query (e.g., "comedy performance decline").
        n_results: Number of document chunks to return (default 5).

    Returns:
        List of relevant document chunks with source and relevance score.
    """
    logger.info(f"Document search: query='{query}', n_results={n_results}")

    results = search_documents(query=query, n_results=min(n_results, 10))

    # Format for clean output
    formatted = []
    for r in results:
        formatted.append({
            "text": r["text"],
            "source_document": r["source"],
            "relevance_score": r["relevance_score"],
            "chunk_index": r["chunk_index"],
        })

    logger.info(f"Document search returned {len(formatted)} results")
    return formatted
