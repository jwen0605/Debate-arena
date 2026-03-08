"""Opponent agent – argues AGAINST the debate topic."""

from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage

from debate_arena.agents.base import DebateAgent
from debate_arena.config import OPPONENT_SYSTEM_PROMPT, DebateConfig
from debate_arena.graph.state import DebateState


class OpponentAgent(DebateAgent):
    """Agent that argues against the given position."""

    def __init__(self, config: DebateConfig | None = None):
        super().__init__(
            role="opponent",
            system_prompt=OPPONENT_SYSTEM_PROMPT,
            config=config,
        )

    def build_prompt(self, state: DebateState, extra_context: str = "") -> list:
        """Inject the advocate's arguments so the opponent can directly counter them."""
        messages = [SystemMessage(content=self.system_prompt)]

        topic = state.get("topic", "")
        current_round = state.get("current_round", 1)
        max_rounds = state.get("max_rounds", 3)
        messages.append(
            HumanMessage(
                content=f"## Debate Topic\n{topic}\n\n"
                f"This is round {current_round} of {max_rounds}."
            )
        )

        # Skill output: research + rebuttal analysis injected before argument generation
        if extra_context:
            messages.append(
                HumanMessage(content=f"## Research & Rebuttal Analysis (use these to strengthen your counter-argument)\n{extra_context}")
            )

        # Advocate's arguments (the opponent MUST see these to counter)
        advocate_args = state.get("advocate_arguments", [])
        if advocate_args:
            history = "\n\n".join(
                f"**Round {a.round_number} – Advocate:**\n{a.content}"
                for a in advocate_args
            )
            messages.append(
                HumanMessage(
                    content=f"## Advocate's Arguments\n{history}\n\n"
                    "Counter the advocate's latest argument. Find weaknesses, "
                    "present opposing evidence, and identify any logical fallacies."
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
