"""Tests for DebateArena core components."""

import pytest
from debate_arena.graph.state import (
    Argument,
    ArgumentScore,
    RoundResult,
    Verdict,
    Citation,
)
from debate_arena.config import DebateConfig


# ──────────────────────────────────────────────
# State model tests
# ──────────────────────────────────────────────

class TestArgumentScore:
    def test_total(self):
        score = ArgumentScore(logic=8, evidence=7, persuasion=9)
        assert score.total == 24

    def test_zero_score(self):
        score = ArgumentScore(logic=0, evidence=0, persuasion=0)
        assert score.total == 0

    def test_max_score(self):
        score = ArgumentScore(logic=10, evidence=10, persuasion=10)
        assert score.total == 30


class TestArgument:
    def test_create_argument(self):
        arg = Argument(
            role="advocate",
            round_number=1,
            content="AI will create more jobs than it destroys.",
        )
        assert arg.role == "advocate"
        assert arg.round_number == 1
        assert arg.citations == []
        assert arg.fallacies == []

    def test_argument_with_citations(self):
        citation = Citation(
            url="https://example.com",
            title="AI Jobs Report",
            snippet="AI expected to create 97M new roles",
        )
        arg = Argument(
            role="opponent",
            round_number=2,
            content="Counter evidence suggests...",
            citations=[citation],
        )
        assert len(arg.citations) == 1
        assert arg.citations[0].title == "AI Jobs Report"


class TestRoundResult:
    def test_round_result(self):
        adv_arg = Argument(role="advocate", round_number=1, content="...")
        opp_arg = Argument(role="opponent", round_number=1, content="...")
        result = RoundResult(
            round_number=1,
            advocate_argument=adv_arg,
            opponent_argument=opp_arg,
            advocate_score=ArgumentScore(logic=7, evidence=8, persuasion=6),
            opponent_score=ArgumentScore(logic=8, evidence=7, persuasion=7),
            judge_feedback="Both sides presented strong arguments.",
            decision="continue",
        )
        assert result.advocate_score.total == 21
        assert result.opponent_score.total == 22
        assert result.decision == "continue"


class TestVerdict:
    def test_verdict(self):
        v = Verdict(
            winner="opponent",
            summary="Opponent presented stronger evidence.",
            total_advocate_score=63,
            total_opponent_score=68,
        )
        assert v.winner == "opponent"
        assert v.total_opponent_score > v.total_advocate_score


# ──────────────────────────────────────────────
# Config tests
# ──────────────────────────────────────────────

class TestDebateConfig:
    def test_defaults(self):
        config = DebateConfig()
        assert config.max_rounds == 3
        assert config.model_name == "claude-sonnet-4-6"
        assert config.human_role is None

    def test_custom_config(self):
        config = DebateConfig(max_rounds=5, model_name="claude-haiku-4-5-20251001", human_role="advocate")
        assert config.max_rounds == 5
        assert config.human_role == "advocate"


# ──────────────────────────────────────────────
# Tool tests (unit-level, mocked)
# ──────────────────────────────────────────────

class TestCitationTool:
    def test_cite_source(self):
        from debate_arena.tools.citation import cite_source

        result = cite_source.invoke({
            "url": "https://example.com/article",
            "title": "Test Article",
            "snippet": "Key finding here",
        })
        assert "Test Article" in result
        assert "https://example.com/article" in result
        assert "Key finding here" in result
