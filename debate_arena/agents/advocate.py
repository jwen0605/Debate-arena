"""Advocate agent – argues IN FAVOR of the debate topic."""

from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage

from debate_arena.agents.base import DebateAgent
from debate_arena.config import ADVOCATE_SYSTEM_PROMPT, DebateConfig
from debate_arena.graph.state import DebateState


class AdvocateAgent(DebateAgent):
    """Agent that argues in favor of the given position."""

    def __init__(self, config: DebateConfig | None = None):
        super().__init__(
            role="advocate",
            system_prompt=ADVOCATE_SYSTEM_PROMPT,
            config=config,
        )

    def build_prompt(self, state: DebateState, extra_context: str = "") -> list:
        """Inject debate history so the advocate can respond to prior arguments."""
        messages = [SystemMessage(content=self.system_prompt)]

        # Topic
        topic = state.get("topic", "")
        current_round = state.get("current_round", 1)
        max_rounds = state.get("max_rounds", 3)
        messages.append(
            HumanMessage(
                content=f"## Debate Topic\n{topic}\n\n"
                f"This is round {current_round} of {max_rounds}."
            )
        )

        # Skill output: research findings injected before argument generation
        if extra_context:
            messages.append(
                HumanMessage(content=f"## Research Findings (use these to support your argument)\n{extra_context}")
            )

        # Previous arguments for context
        opponent_args = state.get("opponent_arguments", [])
        if opponent_args:
            history = "\n\n".join(
                f"**Round {a.round_number} – Opponent:**\n{a.content}"
                for a in opponent_args
            )
            messages.append(
                HumanMessage(
                    content=f"## Opponent's Previous Arguments\n{history}\n\n"
                    "Respond to the opponent's latest points and strengthen your position."
                )
            )
        else:
            messages.append(
                HumanMessage(
                    content="You are opening the debate. Present your strongest opening argument."
                )
            )

        # Judge feedback
        round_results = state.get("round_results", [])
        if round_results:
            latest = round_results[-1]
            messages.append(
                HumanMessage(
                    content=f"## Judge's Feedback from Last Round\n{latest.judge_feedback}\n\n"
                    "Take this feedback into account."
                )
            )

        return messages

    def invoke(self, state: DebateState, extra_context: str = ""):
        messages = self.build_prompt(state, extra_context=extra_context)
        return self.llm.invoke(messages)
