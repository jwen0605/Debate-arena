"""Judge agent – evaluates arguments, scores, and decides debate flow."""

from __future__ import annotations

import json
import re

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

from debate_arena.agents.base import DebateAgent
from debate_arena.config import JUDGE_SYSTEM_PROMPT, DebateConfig
from debate_arena.graph.state import DebateState, ArgumentScore, RoundResult


JUDGE_SCORING_PROMPT = """\
Carefully evaluate each side's argument independently and assign scores that reflect \
which side argued more effectively. The two sides should almost never receive identical scores.

Respond ONLY with valid JSON (no markdown, no extra text):

{
    "advocate_score": {
        "logic": <integer 0-10 for advocate's reasoning quality>,
        "evidence": <integer 0-10 for advocate's use of evidence>,
        "persuasion": <integer 0-10 for advocate's rhetorical effectiveness>
    },
    "opponent_score": {
        "logic": <integer 0-10 for opponent's reasoning quality>,
        "evidence": <integer 0-10 for opponent's use of evidence>,
        "persuasion": <integer 0-10 for opponent's rhetorical effectiveness>
    },
    "feedback": "<2-3 sentences explaining why one side scored higher>",
    "decision": "<continue or conclude>",
    "reasoning": "<why you made this decision>"
}

Decide "conclude" if:
- One side is clearly dominant (>15 point total gap)
- Arguments are becoming repetitive
- Maximum rounds have been reached
"""


class JudgeAgent(DebateAgent):
    """Agent that evaluates both sides and controls debate flow."""

    def __init__(self, config: DebateConfig | None = None):
        super().__init__(
            role="judge",
            system_prompt=JUDGE_SYSTEM_PROMPT,
            config=config,
        )
        # Judge uses low temperature for consistent scoring
        self.scoring_llm = ChatAnthropic(
            model=self.config.model_name,
            temperature=0.1,
        )

    def build_prompt(self, state: DebateState) -> list:
        """Present both sides' latest arguments for evaluation."""
        messages = [SystemMessage(content=self.system_prompt)]

        topic = state.get("topic", "")
        current_round = state.get("current_round", 1)
        max_rounds = state.get("max_rounds", 3)

        messages.append(
            HumanMessage(
                content=f"## Debate Topic\n{topic}\n"
                f"## Round {current_round} of {max_rounds}"
            )
        )

        # Show this round's arguments
        advocate_args = state.get("advocate_arguments", [])
        opponent_args = state.get("opponent_arguments", [])

        if advocate_args:
            latest_adv = advocate_args[-1]
            messages.append(
                HumanMessage(
                    content=f"## Advocate's Argument (Round {latest_adv.round_number})\n"
                    f"{latest_adv.content}"
                )
            )

        if opponent_args:
            latest_opp = opponent_args[-1]
            messages.append(
                HumanMessage(
                    content=f"## Opponent's Argument (Round {latest_opp.round_number})\n"
                    f"{latest_opp.content}"
                )
            )

        # Previous round scores for context
        round_results = state.get("round_results", [])
        if round_results:
            score_history = "\n".join(
                f"Round {r.round_number}: Advocate {r.advocate_score.total} vs Opponent {r.opponent_score.total}"
                for r in round_results
            )
            messages.append(
                HumanMessage(content=f"## Score History\n{score_history}")
            )

        # Force JSON scoring
        messages.append(HumanMessage(content=JUDGE_SCORING_PROMPT))

        return messages

    def score_round(self, state: DebateState) -> RoundResult:
        """Invoke the judge and parse structured scoring output."""
        messages = self.build_prompt(state)
        response = self.scoring_llm.invoke(messages)

        # Parse JSON response
        try:
            data = json.loads(response.content)
        except json.JSONDecodeError:
            # Fallback: extract JSON from markdown code block
            match = re.search(r"```json?\s*(.*?)```", response.content, re.DOTALL)
            if match:
                data = json.loads(match.group(1))
            else:
                # Last resort defaults
                data = {
                    "advocate_score": {"logic": 5, "evidence": 5, "persuasion": 5},
                    "opponent_score": {"logic": 5, "evidence": 5, "persuasion": 5},
                    "feedback": response.content,
                    "decision": "continue",
                    "reasoning": "Could not parse structured output.",
                }

        current_round = state.get("current_round", 1)
        max_rounds = state.get("max_rounds", 3)

        # Force conclude on last round
        decision = data.get("decision", "continue")
        if current_round >= max_rounds:
            decision = "conclude"

        advocate_args = state.get("advocate_arguments", [])
        opponent_args = state.get("opponent_arguments", [])

        return RoundResult(
            round_number=current_round,
            advocate_argument=advocate_args[-1] if advocate_args else None,
            opponent_argument=opponent_args[-1] if opponent_args else None,
            advocate_score=ArgumentScore(**data["advocate_score"]),
            opponent_score=ArgumentScore(**data["opponent_score"]),
            judge_feedback=data.get("feedback", ""),
            decision=decision,
        )
