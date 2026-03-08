"""Debate state definition for LangGraph."""

from __future__ import annotations

import operator
from dataclasses import dataclass, field
from typing import Annotated, Literal, TypedDict


# ──────────────────────────────────────────────
# Data models
# ──────────────────────────────────────────────


@dataclass
class Citation:
    """A cited source."""

    url: str
    title: str
    snippet: str


@dataclass
class ArgumentScore:
    """Score for a single argument."""

    logic: int  # 0-10
    evidence: int  # 0-10
    persuasion: int  # 0-10

    @property
    def total(self) -> int:
        return self.logic + self.evidence + self.persuasion


@dataclass
class Argument:
    """A single argument made by an agent."""

    role: Literal["advocate", "opponent"]
    round_number: int
    content: str
    citations: list[Citation] = field(default_factory=list)
    score: ArgumentScore | None = None
    fallacies: list[str] = field(default_factory=list)


@dataclass
class RoundResult:
    """Result of a single debate round."""

    round_number: int
    advocate_argument: Argument
    opponent_argument: Argument
    advocate_score: ArgumentScore
    opponent_score: ArgumentScore
    judge_feedback: str
    decision: Literal["continue", "conclude"]


@dataclass
class Verdict:
    """Final debate verdict."""

    winner: Literal["advocate", "opponent", "draw"]
    summary: str
    total_advocate_score: int
    total_opponent_score: int


# ──────────────────────────────────────────────
# LangGraph State
# ──────────────────────────────────────────────

def _merge_arguments(existing: list[Argument], new: list[Argument]) -> list[Argument]:
    """Reducer: append new arguments to existing list."""
    return existing + new


def _merge_rounds(existing: list[RoundResult], new: list[RoundResult]) -> list[RoundResult]:
    """Reducer: append new round results."""
    return existing + new


class DebateState(TypedDict):
    """The central state object flowing through the LangGraph debate graph.

    Uses Annotated types with reducers so each node can emit partial
    updates that get merged automatically.
    """

    # ── Immutable config ──
    topic: str
    max_rounds: int

    # ── Round tracking ──
    current_round: Annotated[int, operator.add]

    # ── Arguments (append-only lists) ──
    advocate_arguments: Annotated[list[Argument], _merge_arguments]
    opponent_arguments: Annotated[list[Argument], _merge_arguments]

    # ── Judge results ──
    round_results: Annotated[list[RoundResult], _merge_rounds]

    # ── Control flow ──
    debate_status: Literal["opening", "ongoing", "concluded"]
    next_speaker: Literal["advocate", "opponent", "judge"]

    # ── Final output ──
    verdict: Verdict | None
