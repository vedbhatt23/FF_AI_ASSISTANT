"""
Tool registry: maps tool names to functions, generates OpenAI schemas, dispatches calls.
"""
import json, logging, time
from typing import Any, Callable
from app.models import ToolExecution
from app.tools.sql_tools import (
    compare_titles, get_genre_analytics, get_trending_titles,
    query_marketing_spend, query_movie_performance, query_regional_performance,
    query_reviews_sentiment, query_viewer_demographics, query_watch_activity,
)
from app.tools.doc_tools import search_internal_documents

logger = logging.getLogger(__name__)

TOOL_DEFINITIONS: list[dict] = [
    {"type":"function","function":{"name":"query_movie_performance","description":"Query top movies by revenue/rating. Filters by year/genre.","parameters":{"type":"object","properties":{"year":{"type":"integer","description":"Release year"},"genre":{"type":"string","description":"Genre filter"},"limit":{"type":"integer","description":"Max results","default":10}},"required":[]}}},
    {"type":"function","function":{"name":"query_viewer_demographics","description":"Viewer demographics by city, tier, age, gender.","parameters":{"type":"object","properties":{"city":{"type":"string"},"subscription_tier":{"type":"string"},"age_min":{"type":"integer"},"age_max":{"type":"integer"}},"required":[]}}},
    {"type":"function","function":{"name":"query_watch_activity","description":"Watch activity & engagement: watches, duration, completion rate, unique viewers.","parameters":{"type":"object","properties":{"movie_title":{"type":"string","description":"Movie title (partial match)"},"days":{"type":"integer","default":30},"limit":{"type":"integer","default":20}},"required":[]}}},
    {"type":"function","function":{"name":"query_reviews_sentiment","description":"Reviews & sentiment: counts, avg ratings, sample texts.","parameters":{"type":"object","properties":{"movie_title":{"type":"string"},"min_rating":{"type":"integer"},"limit":{"type":"integer","default":20}},"required":[]}}},
    {"type":"function","function":{"name":"query_marketing_spend","description":"Marketing campaign spend, impressions, clicks, CTR by channel.","parameters":{"type":"object","properties":{"movie_title":{"type":"string"},"channel":{"type":"string"}},"required":[]}}},
    {"type":"function","function":{"name":"query_regional_performance","description":"Regional/city performance: views, revenue, ratings by city and month.","parameters":{"type":"object","properties":{"city":{"type":"string"},"month":{"type":"string","description":"e.g. 2025-04"},"limit":{"type":"integer","default":20}},"required":[]}}},
    {"type":"function","function":{"name":"get_trending_titles","description":"Titles with highest recent watch growth. Shows recent vs previous watches and growth %.","parameters":{"type":"object","properties":{"days":{"type":"integer","default":30},"limit":{"type":"integer","default":10}},"required":[]}}},
    {"type":"function","function":{"name":"compare_titles","description":"Side-by-side comparison of two movies across all metrics.","parameters":{"type":"object","properties":{"title_a":{"type":"string","description":"First movie"},"title_b":{"type":"string","description":"Second movie"}},"required":["title_a","title_b"]}}},
    {"type":"function","function":{"name":"get_genre_analytics","description":"Genre-level aggregations: title count, avg rating, revenue, ROI, watches.","parameters":{"type":"object","properties":{"year":{"type":"integer"}},"required":[]}}},
    {"type":"function","function":{"name":"search_internal_documents","description":"Semantic search over internal docs (quarterly reports, campaign summaries, roadmap, policies, audience reports).","parameters":{"type":"object","properties":{"query":{"type":"string","description":"Search query"},"n_results":{"type":"integer","default":5}},"required":["query"]}}},
]

TOOL_FUNCTIONS: dict[str, Callable] = {
    "query_movie_performance": query_movie_performance,
    "query_viewer_demographics": query_viewer_demographics,
    "query_watch_activity": query_watch_activity,
    "query_reviews_sentiment": query_reviews_sentiment,
    "query_marketing_spend": query_marketing_spend,
    "query_regional_performance": query_regional_performance,
    "get_trending_titles": get_trending_titles,
    "compare_titles": compare_titles,
    "get_genre_analytics": get_genre_analytics,
    "search_internal_documents": search_internal_documents,
}

TOOL_SOURCE_MAP: dict[str, str] = {
    "query_movie_performance": "sql_database",
    "query_viewer_demographics": "sql_database",
    "query_watch_activity": "sql_database",
    "query_reviews_sentiment": "sql_database",
    "query_marketing_spend": "sql_database",
    "query_regional_performance": "sql_database",
    "get_trending_titles": "sql_database",
    "compare_titles": "sql_database",
    "get_genre_analytics": "sql_database",
    "search_internal_documents": "vector_store",
}


def dispatch_tool(name: str, arguments: dict[str, Any]) -> tuple[Any, ToolExecution]:
    """Dispatch a tool call, capturing timing and metadata."""
    if name not in TOOL_FUNCTIONS:
        raise ValueError(f"Unknown tool: {name}")
    func = TOOL_FUNCTIONS[name]
    source_type = TOOL_SOURCE_MAP.get(name, "unknown")
    start = time.perf_counter()
    try:
        result = func(**arguments)
        elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
        if isinstance(result, list):
            row_count = len(result)
            summary = f"Returned {row_count} results"
            if row_count > 0 and isinstance(result[0], dict):
                keys = list(result[0].keys())[:4]
                summary += f" with fields: {', '.join(keys)}"
        else:
            row_count = 1
            summary = f"Returned result: {str(result)[:200]}"
        execution = ToolExecution(
            tool_name=name, arguments=arguments, result_summary=summary,
            source_type=source_type, execution_time_ms=elapsed_ms, row_count=row_count,
        )
        logger.info(f"Tool '{name}' executed in {elapsed_ms}ms -> {summary}")
        return result, execution
    except Exception as e:
        elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
        logger.error(f"Tool '{name}' failed: {e}")
        execution = ToolExecution(
            tool_name=name, arguments=arguments, result_summary=f"Error: {str(e)[:200]}",
            source_type=source_type, execution_time_ms=elapsed_ms, row_count=0,
        )
        return {"error": str(e)}, execution


def get_tool_definitions() -> list[dict]:
    """Get all tool definitions in OpenAI function calling format."""
    return TOOL_DEFINITIONS
