"""Base agent class shared by Advocate, Opponent, and Judge."""

from __future__ import annotations

from langchain_anthropic import ChatAnthropic

from debate_arena.config import DebateConfig


class DebateAgent:
    """Base class for all debate agents."""

    def __init__(
        self,
        role: str,
        system_prompt: str,
        config: DebateConfig | None = None,
    ):
        self.role = role
        self.system_prompt = system_prompt
        self.config = config or DebateConfig()

        self.llm = ChatAnthropic(
            model=self.config.model_name,
            temperature=self.config.temperature,
        )

    def build_prompt(self, state) -> list:
        """Build the message list to send to the LLM. Override in subclasses."""
        raise NotImplementedError

    def invoke(self, state):
        """Invoke the agent with the current debate state."""
        messages = self.build_prompt(state)
        return self.llm.invoke(messages)
