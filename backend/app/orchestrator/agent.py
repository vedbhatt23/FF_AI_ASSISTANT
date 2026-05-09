"""
AI Orchestrator — OpenAI function-calling loop.
Takes user messages, routes through LLM with tool definitions,
dispatches tool calls, and returns synthesized responses.
"""
import json, logging, uuid
from typing import Any, Optional
from openai import OpenAI
from app.config import get_settings
from app.models import ChatRequest, ChatResponse, ChartData, ToolExecution
from app.tools.registry import dispatch_tool, get_tool_definitions

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are an AI analytics assistant for an entertainment company. You help leadership answer business questions using internal data and documents.

RULES:
1. Always use the provided tools to look up data. Never fabricate numbers or statistics.
2. When answering, cite which data sources you used.
3. For numerical/comparative questions, present data in a structured way (tables, lists).
4. When data supports visualization, suggest it clearly (e.g., "Here's a comparison chart").
5. For strategic/recommendation questions, combine data insights with internal document context.
6. Be concise but thorough. Leadership values actionable insights.
7. If a question is ambiguous, make reasonable assumptions and state them.
8. Never expose raw database queries, internal system details, or viewer PII.
9. When comparing items, use ALL relevant metrics for a holistic view.
10. For trend analysis, consider both recent activity and historical context.

AVAILABLE DATA SOURCES:
- SQL Database: movies, viewers, watch_activity, reviews, marketing_spend, regional_performance
- Internal Documents: quarterly reports, campaign summaries, content roadmap, policy guidelines, audience behavior reports

When you have numerical comparison data suitable for a chart, format a JSON block like:
```chart
{"chart_type": "bar|line|pie|area", "title": "Chart Title", "data": [...], "x_key": "field", "y_keys": ["field1", "field2"]}
```"""

MAX_TOOL_ROUNDS = 5


def _extract_chart_data(text: str) -> tuple[str, Optional[ChartData]]:
    """Extract chart JSON from response text if present."""
    import re
    pattern = r"```chart\s*\n(.*?)\n```"
    match = re.search(pattern, text, re.DOTALL)
    if not match:
        return text, None
    try:
        chart_json = json.loads(match.group(1))
        chart = ChartData(
            chart_type=chart_json.get("chart_type", "bar"),
            title=chart_json.get("title", "Chart"),
            data=chart_json.get("data", []),
            x_key=chart_json.get("x_key", "name"),
            y_keys=chart_json.get("y_keys", ["value"]),
            colors=chart_json.get("colors"),
        )
        clean_text = text[:match.start()] + text[match.end():]
        return clean_text.strip(), chart
    except (json.JSONDecodeError, Exception) as e:
        logger.warning(f"Failed to parse chart data: {e}")
        return text, None


def _auto_generate_chart(tool_executions: list[tuple[str, Any, ToolExecution]]) -> Optional[ChartData]:
    """Auto-generate chart data from tool results when appropriate."""
    for tool_name, result, meta in tool_executions:
        if not isinstance(result, list) or len(result) < 2:
            continue
        if tool_name == "get_genre_analytics":
            return ChartData(
                chart_type="bar", title="Genre Performance",
                data=[{"genre": r.get("genre",""), "revenue": r.get("total_revenue",0)/1e6, "avg_rating": r.get("avg_rating",0)} for r in result],
                x_key="genre", y_keys=["revenue"], colors=["#3B82F6","#8B5CF6"]
            )
        if tool_name == "compare_titles" and len(result) == 2:
            return ChartData(
                chart_type="bar", title=f"{result[0].get('title','')} vs {result[1].get('title','')}",
                data=[{"metric":"Revenue ($M)","A":result[0].get("revenue",0)/1e6,"B":result[1].get("revenue",0)/1e6},
                      {"metric":"Rating","A":result[0].get("movie_rating",0),"B":result[1].get("movie_rating",0)},
                      {"metric":"Watches","A":result[0].get("total_watches",0),"B":result[1].get("total_watches",0)}],
                x_key="metric", y_keys=["A","B"],
                colors=["#3B82F6","#8B5CF6"]
            )
        if tool_name == "get_trending_titles":
            return ChartData(
                chart_type="bar", title="Trending Titles",
                data=[{"title": r.get("title","")[:20], "watches": r.get("recent_watches",0)} for r in result[:10]],
                x_key="title", y_keys=["watches"], colors=["#3B82F6"]
            )
        if tool_name == "query_regional_performance":
            city_data: dict[str, int] = {}
            for r in result:
                c = r.get("city","")
                city_data[c] = city_data.get(c,0) + r.get("views",0)
            if len(city_data) >= 2:
                return ChartData(
                    chart_type="bar", title="Regional Performance",
                    data=[{"city":c,"views":v} for c,v in sorted(city_data.items(), key=lambda x:-x[1])],
                    x_key="city", y_keys=["views"], colors=["#3B82F6"]
                )
        if tool_name == "query_movie_performance":
            return ChartData(
                chart_type="bar", title="Movie Performance",
                data=[{"title": r.get("title","")[:20], "revenue": r.get("revenue",0)/1e6, "rating": r.get("rating",0)} for r in result[:10]],
                x_key="title", y_keys=["revenue"], colors=["#3B82F6","#8B5CF6"]
            )
    return None


async def process_chat(request: ChatRequest) -> ChatResponse:
    """Main orchestration: user message -> LLM -> tool calls -> response."""
    settings = get_settings()
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    conversation_id = request.conversation_id or str(uuid.uuid4())
    all_tool_executions: list[ToolExecution] = []
    tool_results_for_chart: list[tuple[str, Any, ToolExecution]] = []

    # Build initial messages
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": request.message},
    ]
    if request.filters:
        messages[-1]["content"] += f"\n\n[Active filters: {json.dumps(request.filters)}]"

    # Function calling loop
    for round_num in range(MAX_TOOL_ROUNDS):
        logger.info(f"Orchestrator round {round_num + 1}")
        try:
            response = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=messages,
                tools=get_tool_definitions(),
                tool_choice="auto",
                temperature=0.3,
                max_tokens=2000,
            )
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return ChatResponse(
                answer=f"I encountered an error communicating with the AI service. Please try again. Error: {str(e)[:100]}",
                conversation_id=conversation_id,
                sources=all_tool_executions,
            )

        choice = response.choices[0]

        # If no tool calls, we have the final answer
        if choice.finish_reason == "stop" or not choice.message.tool_calls:
            answer_text = choice.message.content or "I couldn't generate a response."
            clean_text, chart = _extract_chart_data(answer_text)
            if chart is None:
                chart = _auto_generate_chart(tool_results_for_chart)
            return ChatResponse(
                answer=clean_text, conversation_id=conversation_id,
                sources=all_tool_executions, chart_data=chart,
            )

        # Process tool calls
        messages.append(choice.message.model_dump())
        for tool_call in choice.message.tool_calls:
            fn_name = tool_call.function.name
            try:
                fn_args = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError:
                fn_args = {}
            logger.info(f"Tool call: {fn_name}({fn_args})")
            result, execution = dispatch_tool(fn_name, fn_args)
            all_tool_executions.append(execution)
            tool_results_for_chart.append((fn_name, result, execution))
            result_str = json.dumps(result, default=str)
            if len(result_str) > 4000:
                result_str = result_str[:4000] + "... (truncated)"
            messages.append({
                "role": "tool", "tool_call_id": tool_call.id, "content": result_str,
            })

    # Max rounds exceeded
    return ChatResponse(
        answer="I gathered extensive data but reached the processing limit. Here's what I found based on the tools executed.",
        conversation_id=conversation_id,
        sources=all_tool_executions,
        chart_data=_auto_generate_chart(tool_results_for_chart),
    )
