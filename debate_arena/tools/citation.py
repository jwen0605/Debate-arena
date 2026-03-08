"""Source citation tool."""

from langchain_core.tools import tool


@tool
def cite_source(url: str, title: str, snippet: str) -> str:
    """Formally cite a source in your argument.

    Use this after finding evidence with web_search to create a proper citation.

    Args:
        url: The URL of the source.
        title: The title of the article or page.
        snippet: The relevant excerpt from the source.

    Returns:
        A formatted citation string.
    """
    return f"[{title}]({url})\n> {snippet}"
