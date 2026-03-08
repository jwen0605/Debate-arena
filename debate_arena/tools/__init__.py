"""Tool registry for each agent role."""

from debate_arena.tools.search import web_search
from debate_arena.tools.logic import logical_analysis
from debate_arena.tools.citation import cite_source

ADVOCATE_TOOLS = [web_search, cite_source]
OPPONENT_TOOLS = [web_search, cite_source, logical_analysis]
JUDGE_TOOLS = [logical_analysis]

__all__ = ["web_search", "cite_source", "logical_analysis",
           "ADVOCATE_TOOLS", "OPPONENT_TOOLS", "JUDGE_TOOLS"]
