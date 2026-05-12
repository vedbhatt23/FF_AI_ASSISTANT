"""
SQL-based tools for structured data queries.
Each tool is a scoped, parameterized function that the LLM can call.
No raw SQL access is exposed to the LLM.
"""

import logging
from typing import Any, Optional

from app.database import execute_safe_query

logger = logging.getLogger(__name__)


def query_movie_performance(
    year: Optional[int] = None,
    genre: Optional[str] = None,
    limit: int = 10,
) -> list[dict[str, Any]]:
    """
    Query top-performing movies by revenue and rating.

    Args:
        year: Filter by release year (e.g., 2025).
        genre: Filter by genre (e.g., "Sci-Fi", "Action").
        limit: Maximum number of results (default 10).
    """
    conditions = []
    params: list[Any] = []

    if year:
        conditions.append("CAST(strftime('%Y', release_date) AS INTEGER) = ?")
        params.append(year)
    if genre:
        conditions.append("LOWER(genre) = LOWER(?)")
        params.append(genre)

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    params.append(min(limit, 50))

    sql = f"""
        SELECT movie_id, title, genre, release_date, budget, revenue, rating, director,
               CASE WHEN budget > 0 THEN ROUND(CAST(revenue AS REAL) / budget, 2) ELSE 0 END as roi
        FROM movies
        {where_clause}
        ORDER BY revenue DESC
        LIMIT ?
    """
    return execute_safe_query(sql, params)


def query_viewer_demographics(
    city: Optional[str] = None,
    subscription_tier: Optional[str] = None,
    age_min: Optional[int] = None,
    age_max: Optional[int] = None,
) -> list[dict[str, Any]]:
    """
    Query viewer demographics breakdown.

    Args:
        city: Filter by city name.
        subscription_tier: Filter by tier (Free, Basic, Premium, VIP).
        age_min: Minimum age filter.
        age_max: Maximum age filter.
    """
    conditions = []
    params: list[Any] = []

    if city:
        conditions.append("LOWER(city) = LOWER(?)")
        params.append(city)
    if subscription_tier:
        conditions.append("LOWER(subscription_tier) = LOWER(?)")
        params.append(subscription_tier)
    if age_min:
        conditions.append("age >= ?")
        params.append(age_min)
    if age_max:
        conditions.append("age <= ?")
        params.append(age_max)

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

    sql = f"""
        SELECT city,
               subscription_tier,
               COUNT(*) as viewer_count,
               ROUND(AVG(age), 1) as avg_age,
               gender,
               COUNT(*) as count
        FROM viewers
        {where_clause}
        GROUP BY city, subscription_tier, gender
        ORDER BY viewer_count DESC
    """
    return execute_safe_query(sql, params)


def query_watch_activity(
    movie_title: Optional[str] = None,
    days: int = 30,
    limit: int = 20,
) -> list[dict[str, Any]]:
    """
    Query watch activity and engagement metrics.

    Args:
        movie_title: Filter by movie title (partial match).
        days: Number of recent days to look back (default 30).
        limit: Maximum results.
    """
    params: list[Any] = []
    movie_join_cond = ""

    if movie_title:
        movie_join_cond = "AND LOWER(m.title) LIKE LOWER(?)"
        params.append(f"%{movie_title}%")

    params.append(days)
    params.append(min(limit, 50))

    sql = f"""
        SELECT m.title, m.genre,
               COUNT(wa.activity_id) as total_watches,
               ROUND(AVG(wa.watch_duration_mins), 1) as avg_duration_mins,
               ROUND(AVG(CASE WHEN wa.completed THEN 1.0 ELSE 0.0 END) * 100, 1) as completion_rate_pct,
               wa.device,
               COUNT(DISTINCT wa.viewer_id) as unique_viewers
        FROM watch_activity wa
        JOIN movies m ON wa.movie_id = m.movie_id
        WHERE wa.watch_date >= date('2025-05-01', '-' || ? || ' days')
        {movie_join_cond}
        GROUP BY m.title, m.genre, wa.device
        ORDER BY total_watches DESC
        LIMIT ?
    """
    return execute_safe_query(sql, params)


def query_reviews_sentiment(
    movie_title: Optional[str] = None,
    min_rating: Optional[int] = None,
    limit: int = 20,
) -> list[dict[str, Any]]:
    """
    Query reviews and sentiment for movies.

    Args:
        movie_title: Filter by movie title (partial match).
        min_rating: Minimum review rating filter.
        limit: Maximum results.
    """
    conditions = []
    params: list[Any] = []

    if movie_title:
        conditions.append("LOWER(m.title) LIKE LOWER(?)")
        params.append(f"%{movie_title}%")
    if min_rating:
        conditions.append("r.rating >= ?")
        params.append(min_rating)

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    params.append(min(limit, 50))

    sql = f"""
        SELECT m.title, m.genre,
               COUNT(r.review_id) as review_count,
               ROUND(AVG(r.rating), 2) as avg_rating,
               MIN(r.rating) as min_rating,
               MAX(r.rating) as max_rating,
               GROUP_CONCAT(r.review_text, ' | ') as sample_reviews
        FROM reviews r
        JOIN movies m ON r.movie_id = m.movie_id
        {where_clause}
        GROUP BY m.title, m.genre
        ORDER BY avg_rating DESC
        LIMIT ?
    """
    results = execute_safe_query(sql, params)

    # Truncate sample reviews to avoid huge payloads
    for r in results:
        if r.get("sample_reviews"):
            reviews = r["sample_reviews"].split(" | ")[:3]
            r["sample_reviews"] = " | ".join(reviews)

    return results


def query_marketing_spend(
    movie_title: Optional[str] = None,
    channel: Optional[str] = None,
) -> list[dict[str, Any]]:
    """
    Query marketing spend and campaign ROI data.

    Args:
        movie_title: Filter by movie title.
        channel: Filter by marketing channel.
    """
    conditions = []
    params: list[Any] = []

    if movie_title:
        conditions.append("LOWER(m.title) LIKE LOWER(?)")
        params.append(f"%{movie_title}%")
    if channel:
        conditions.append("LOWER(ms.channel) = LOWER(?)")
        params.append(channel)

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

    sql = f"""
        SELECT m.title, ms.channel,
               SUM(ms.spend_amount) as total_spend,
               SUM(ms.impressions) as total_impressions,
               SUM(ms.clicks) as total_clicks,
               CASE WHEN SUM(ms.impressions) > 0
                    THEN ROUND(CAST(SUM(ms.clicks) AS REAL) / SUM(ms.impressions) * 100, 2)
                    ELSE 0 END as ctr_pct,
               ms.start_date, ms.end_date
        FROM marketing_spend ms
        JOIN movies m ON ms.movie_id = m.movie_id
        {where_clause}
        GROUP BY m.title, ms.channel
        ORDER BY total_spend DESC
    """
    return execute_safe_query(sql, params)


def query_regional_performance(
    city: Optional[str] = None,
    month: Optional[str] = None,
    limit: int = 20,
) -> list[dict[str, Any]]:
    """
    Query regional/city-level performance data.

    Args:
        city: Filter by city name.
        month: Filter by month (e.g., '2025-04').
        limit: Maximum results.
    """
    conditions = []
    params: list[Any] = []

    if city:
        conditions.append("LOWER(rp.city) = LOWER(?)")
        params.append(city)
    if month:
        conditions.append("rp.month = ?")
        params.append(month)

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    params.append(min(limit, 50))

    sql = f"""
        SELECT rp.city, m.title, m.genre,
               rp.views, rp.revenue, rp.avg_rating, rp.month
        FROM regional_performance rp
        JOIN movies m ON rp.movie_id = m.movie_id
        {where_clause}
        ORDER BY rp.views DESC
        LIMIT ?
    """
    return execute_safe_query(sql, params)


def get_trending_titles(days: int = 30, limit: int = 10) -> list[dict[str, Any]]:
    """
    Get titles with the highest recent watch activity growth.

    Args:
        days: Number of recent days to analyze (default 30).
        limit: Number of trending titles to return.
    """
    params = [days, 2 * days, days, min(limit, 20)]

    sql = """
        SELECT m.title, m.genre, m.rating,
               recent.watch_count as recent_watches,
               COALESCE(older.watch_count, 0) as previous_watches,
               CASE WHEN COALESCE(older.watch_count, 0) > 0
                    THEN ROUND((CAST(recent.watch_count AS REAL) - older.watch_count) / older.watch_count * 100, 1)
                    ELSE 100.0 END as growth_pct,
               recent.unique_viewers
        FROM movies m
        JOIN (
            SELECT movie_id,
                   COUNT(*) as watch_count,
                   COUNT(DISTINCT viewer_id) as unique_viewers
            FROM watch_activity
            WHERE watch_date >= date('2025-05-01', '-' || ? || ' days')
            GROUP BY movie_id
        ) recent ON m.movie_id = recent.movie_id
        LEFT JOIN (
            SELECT movie_id,
                   COUNT(*) as watch_count
            FROM watch_activity
            WHERE watch_date >= date('2025-05-01', '-' || ? || ' days')
              AND watch_date < date('2025-05-01', '-' || ? || ' days')
            GROUP BY movie_id
        ) older ON m.movie_id = older.movie_id
        ORDER BY recent.watch_count DESC
        LIMIT ?
    """
    return execute_safe_query(sql, params)


def compare_titles(title_a: str, title_b: str) -> list[dict[str, Any]]:
    """
    Side-by-side comparison of two movie titles across all metrics.

    Args:
        title_a: First movie title.
        title_b: Second movie title.
    """
    params = [f"%{title_a}%", f"%{title_b}%"]

    sql = """
        SELECT
            m.title,
            m.genre,
            m.release_date,
            m.budget,
            m.revenue,
            m.rating as movie_rating,
            CASE WHEN m.budget > 0 THEN ROUND(CAST(m.revenue AS REAL) / m.budget, 2) ELSE 0 END as roi,
            COALESCE(wa.total_watches, 0) as total_watches,
            COALESCE(wa.avg_duration, 0) as avg_watch_duration_mins,
            COALESCE(wa.completion_rate, 0) as completion_rate_pct,
            COALESCE(wa.unique_viewers, 0) as unique_viewers,
            COALESCE(rv.review_count, 0) as review_count,
            COALESCE(rv.avg_review_rating, 0) as avg_review_rating,
            COALESCE(mk.total_marketing_spend, 0) as total_marketing_spend
        FROM movies m
        LEFT JOIN (
            SELECT movie_id,
                   COUNT(*) as total_watches,
                   ROUND(AVG(watch_duration_mins), 1) as avg_duration,
                   ROUND(AVG(CASE WHEN completed THEN 1.0 ELSE 0.0 END) * 100, 1) as completion_rate,
                   COUNT(DISTINCT viewer_id) as unique_viewers
            FROM watch_activity GROUP BY movie_id
        ) wa ON m.movie_id = wa.movie_id
        LEFT JOIN (
            SELECT movie_id,
                   COUNT(*) as review_count,
                   ROUND(AVG(rating), 2) as avg_review_rating
            FROM reviews GROUP BY movie_id
        ) rv ON m.movie_id = rv.movie_id
        LEFT JOIN (
            SELECT movie_id,
                   SUM(spend_amount) as total_marketing_spend
            FROM marketing_spend GROUP BY movie_id
        ) mk ON m.movie_id = mk.movie_id
        WHERE LOWER(m.title) LIKE LOWER(?) OR LOWER(m.title) LIKE LOWER(?)
    """
    return execute_safe_query(sql, params)


def get_genre_analytics(year: Optional[int] = None) -> list[dict[str, Any]]:
    """
    Get genre-level performance aggregations.

    Args:
        year: Filter by release year.
    """
    conditions = []
    params: list[Any] = []

    if year:
        conditions.append("CAST(strftime('%Y', m.release_date) AS INTEGER) = ?")
        params.append(year)

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

    sql = f"""
        SELECT m.genre,
               COUNT(DISTINCT m.movie_id) as title_count,
               ROUND(AVG(m.rating), 2) as avg_rating,
               SUM(m.revenue) as total_revenue,
               SUM(m.budget) as total_budget,
               CASE WHEN SUM(m.budget) > 0
                    THEN ROUND(CAST(SUM(m.revenue) AS REAL) / SUM(m.budget), 2)
                    ELSE 0 END as avg_roi,
               COALESCE(wa.total_watches, 0) as total_watches,
               COALESCE(wa.avg_completion, 0) as avg_completion_rate_pct
        FROM movies m
        LEFT JOIN (
            SELECT movie_id,
                   COUNT(*) as total_watches,
                   ROUND(AVG(CASE WHEN completed THEN 1.0 ELSE 0.0 END) * 100, 1) as avg_completion
            FROM watch_activity GROUP BY movie_id
        ) wa ON m.movie_id = wa.movie_id
        {where_clause}
        GROUP BY m.genre
        ORDER BY total_revenue DESC
    """
    return execute_safe_query(sql, params)
