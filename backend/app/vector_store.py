"""
ChromaDB vector store for document search.
Handles document chunking, embedding, and semantic search.
"""

import logging
from typing import Any

import chromadb
from chromadb.config import Settings as ChromaSettings

from app.config import get_settings

logger = logging.getLogger(__name__)

_client: chromadb.ClientAPI | None = None
_collection: chromadb.Collection | None = None


def get_client() -> chromadb.ClientAPI:
    """Get or create ChromaDB persistent client."""
    global _client
    if _client is None:
        settings = get_settings()
        _client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIR,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        logger.info(f"ChromaDB client initialized at: {settings.CHROMA_PERSIST_DIR}")
    return _client


def get_collection() -> chromadb.Collection:
    """Get or create the internal documents collection."""
    global _collection
    if _collection is None:
        client = get_client()
        settings = get_settings()
        _collection = client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION_NAME,
            metadata={"description": "Internal company documents for semantic search"},
        )
        logger.info(f"ChromaDB collection ready: {settings.CHROMA_COLLECTION_NAME}")
    return _collection


def add_documents(
    documents: list[str],
    metadatas: list[dict[str, Any]],
    ids: list[str],
) -> None:
    """Add document chunks to the collection."""
    collection = get_collection()
    collection.add(documents=documents, metadatas=metadatas, ids=ids)
    logger.info(f"Added {len(documents)} chunks to ChromaDB")


def search_documents(query: str, n_results: int = 5) -> list[dict[str, Any]]:
    """
    Semantic search over the document collection.

    Args:
        query: Natural language search query.
        n_results: Number of results to return.

    Returns:
        List of result dictionaries with keys: text, source, relevance_score
    """
    collection = get_collection()

    if collection.count() == 0:
        logger.warning("ChromaDB collection is empty")
        return []

    results = collection.query(query_texts=[query], n_results=min(n_results, collection.count()))

    search_results = []
    if results and results["documents"]:
        for i, doc in enumerate(results["documents"][0]):
            metadata = results["metadatas"][0][i] if results["metadatas"] else {}
            distance = results["distances"][0][i] if results["distances"] else 0.0
            # Convert distance to similarity score (ChromaDB uses L2 distance)
            relevance = round(max(0, 1 - distance / 2), 4)

            search_results.append({
                "text": doc,
                "source": metadata.get("source", "unknown"),
                "chunk_index": metadata.get("chunk_index", 0),
                "relevance_score": relevance,
            })

    return search_results


def get_collection_count() -> int:
    """Get the number of documents in the collection."""
    try:
        return get_collection().count()
    except Exception:
        return 0


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> list[str]:
    """
    Split text into overlapping chunks for embedding.

    Args:
        text: Full document text.
        chunk_size: Target characters per chunk.
        overlap: Number of overlapping characters between chunks.

    Returns:
        List of text chunks.
    """
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size

        # Try to break at sentence boundary
        if end < len(text):
            # Look for period, newline, or other sentence endings
            for sep in ["\n\n", "\n", ". ", "! ", "? "]:
                last_sep = text[start:end].rfind(sep)
                if last_sep > chunk_size * 0.5:
                    end = start + last_sep + len(sep)
                    break

        chunks.append(text[start:end].strip())
        start = end - overlap

    return [c for c in chunks if c]
