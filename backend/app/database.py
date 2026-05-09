"""
SQLite database connection and query utilities.
All queries are parameterized to prevent SQL injection.
"""

import logging
import sqlite3
from pathlib import Path
from typing import Any

from app.config import get_settings

logger = logging.getLogger(__name__)

_connection: sqlite3.Connection | None = None


def get_connection() -> sqlite3.Connection:
    """Get or create SQLite connection (singleton per process)."""
    global _connection
    if _connection is None:
        db_path = Path(get_settings().DATABASE_PATH)
        db_path.parent.mkdir(parents=True, exist_ok=True)
        _connection = sqlite3.connect(str(db_path), check_same_thread=False)
        _connection.row_factory = sqlite3.Row
        _connection.execute("PRAGMA journal_mode=WAL")
        _connection.execute("PRAGMA foreign_keys=ON")
        logger.info(f"SQLite connection established: {db_path}")
    return _connection


def execute_safe_query(
    sql: str, params: tuple | list = (), fetch: str = "all"
) -> list[dict[str, Any]]:
    """
    Execute a parameterized SQL query safely.

    Args:
        sql: SQL query with ? placeholders for parameters.
        params: Tuple or list of parameter values.
        fetch: 'all' for fetchall, 'one' for fetchone.

    Returns:
        List of row dictionaries.
    """
    conn = get_connection()
    try:
        cursor = conn.execute(sql, params)
        if fetch == "one":
            row = cursor.fetchone()
            return [dict(row)] if row else []
        else:
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    except sqlite3.Error as e:
        logger.error(f"SQL error: {e} | Query: {sql} | Params: {params}")
        raise


def execute_write(sql: str, params: tuple | list = ()) -> int:
    """Execute a write operation (INSERT/UPDATE/DELETE). Returns affected rows."""
    conn = get_connection()
    try:
        cursor = conn.execute(sql, params)
        conn.commit()
        return cursor.rowcount
    except sqlite3.Error as e:
        logger.error(f"SQL write error: {e} | Query: {sql}")
        conn.rollback()
        raise


def execute_many(sql: str, data: list[tuple]) -> int:
    """Execute many inserts at once. Returns total rows affected."""
    conn = get_connection()
    try:
        cursor = conn.executemany(sql, data)
        conn.commit()
        return cursor.rowcount
    except sqlite3.Error as e:
        logger.error(f"SQL executemany error: {e}")
        conn.rollback()
        raise


def init_db():
    """Initialize database tables."""
    conn = get_connection()

    tables = [
        """
        CREATE TABLE IF NOT EXISTS movies (
            movie_id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            genre TEXT NOT NULL,
            release_date TEXT,
            budget INTEGER,
            revenue INTEGER,
            rating REAL,
            director TEXT,
            language TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS viewers (
            viewer_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            city TEXT,
            subscription_tier TEXT,
            signup_date TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS watch_activity (
            activity_id INTEGER PRIMARY KEY,
            viewer_id INTEGER,
            movie_id INTEGER,
            watch_date TEXT,
            watch_duration_mins INTEGER,
            completed BOOLEAN,
            device TEXT,
            FOREIGN KEY (viewer_id) REFERENCES viewers(viewer_id),
            FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS reviews (
            review_id INTEGER PRIMARY KEY,
            viewer_id INTEGER,
            movie_id INTEGER,
            rating INTEGER,
            review_text TEXT,
            review_date TEXT,
            FOREIGN KEY (viewer_id) REFERENCES viewers(viewer_id),
            FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS marketing_spend (
            campaign_id INTEGER PRIMARY KEY,
            movie_id INTEGER,
            channel TEXT,
            spend_amount INTEGER,
            impressions INTEGER,
            clicks INTEGER,
            start_date TEXT,
            end_date TEXT,
            FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS regional_performance (
            region_id INTEGER PRIMARY KEY,
            movie_id INTEGER,
            city TEXT,
            views INTEGER,
            revenue INTEGER,
            avg_rating REAL,
            month TEXT,
            FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
        )
        """,
    ]

    for ddl in tables:
        conn.execute(ddl)
    conn.commit()
    logger.info("Database tables initialized")


def get_table_counts() -> dict[str, int]:
    """Get row counts for all tables (used for health checks)."""
    tables = ["movies", "viewers", "watch_activity", "reviews", "marketing_spend", "regional_performance"]
    counts = {}
    for table in tables:
        result = execute_safe_query(f"SELECT COUNT(*) as count FROM {table}")
        counts[table] = result[0]["count"] if result else 0
    return counts


def close_connection():
    """Close the database connection."""
    global _connection
    if _connection:
        _connection.close()
        _connection = None
        logger.info("SQLite connection closed")
