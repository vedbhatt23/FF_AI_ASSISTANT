"""
Data ingestion script — standalone entry point.
Loads CSVs into SQLite and documents into ChromaDB.
"""
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.routers.ingest import _load_csvs, _load_documents
from app.database import get_table_counts
from app.vector_store import get_collection_count


def main():
    print("📥 Starting data ingestion...\n")

    print("Loading CSVs into SQLite...")
    _load_csvs()
    counts = get_table_counts()
    for table, count in counts.items():
        print(f"  ✅ {table}: {count} rows")

    print("\nLoading documents into ChromaDB...")
    _load_documents()
    doc_count = get_collection_count()
    print(f"  ✅ {doc_count} document chunks indexed")

    print(f"\n✅ Ingestion complete!")


if __name__ == "__main__":
    main()
