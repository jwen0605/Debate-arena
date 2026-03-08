"""Logical fallacy detection tool."""

from langchain_core.tools import tool
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage
import os

FALLACY_DETECTION_PROMPT = """\
You are a logic expert. Analyze the following argument for logical fallacies.

Common fallacies to check for:
- Straw Man: Misrepresenting the opponent's argument
- Ad Hominem: Attacking the person instead of the argument
- Appeal to Authority: Using authority as evidence without proper justification
- False Dichotomy: Presenting only two options when more exist
- Slippery Slope: Assuming one event will lead to extreme consequences
- Circular Reasoning: Using the conclusion as a premise
- Red Herring: Introducing irrelevant information
- Hasty Generalization: Drawing broad conclusions from limited examples
- Appeal to Emotion: Using emotional manipulation instead of logic
- Burden of Proof: Shifting the burden of proof incorrectly

Respond in JSON format:
{
    "fallacies_found": [
        {
            "type": "fallacy name",
            "explanation": "brief explanation of how this fallacy appears",
            "quote": "the specific part that contains the fallacy"
        }
    ],
    "overall_logical_soundness": "strong | moderate | weak",
    "notes": "any additional observations"
}

If no fallacies are found, return an empty list for fallacies_found.
"""


@tool
def logical_analysis(argument: str) -> str:
    """Analyze an argument for logical fallacies and reasoning errors.

    Use this to identify weaknesses in the opponent's reasoning,
    such as straw man arguments, false dichotomies, or appeal to emotion.

    Args:
        argument: The argument text to analyze.

    Returns:
        A JSON report of detected logical fallacies.
    """
    llm = ChatAnthropic(
        model="claude-haiku-4-5-20251001",
        temperature=0,
        api_key=os.getenv("ANTHROPIC_API_KEY"),
    )
    response = llm.invoke([
        SystemMessage(content=FALLACY_DETECTION_PROMPT),
        HumanMessage(content=f"Analyze this argument:\n\n{argument}"),
    ])
    return response.content
