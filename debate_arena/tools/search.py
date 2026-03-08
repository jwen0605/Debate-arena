"""Web search tool using Tavily API."""

from langchain_core.tools import tool
from tavily import TavilyClient
import os


@tool
def web_search(query: str) -> str:
    """Search the web for current information on a topic.

    Use this to find evidence, statistics, expert opinions,
    and recent news to support or counter arguments.

    Args:
        query: The search query string.

    Returns:
        Formatted search results with titles, snippets, and URLs.
    """
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    results = client.search(query, max_results=5)

    formatted = []
    for r in results.get("results", []):
        formatted.append(
            f"**{r['title']}**\n"
            f"URL: {r['url']}\n"
            f"Snippet: {r['content']}\n"
        )
    return "\n---\n".join(formatted) if formatted else "No results found."
