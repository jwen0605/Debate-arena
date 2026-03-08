"""LangGraph StateGraph – the core debate orchestration engine.

This module wires together the three agents (Advocate, Opponent, Judge)
into a cyclic graph with conditional routing based on the Judge's decisions.

Graph structure:
    START → advocate_node → opponent_node → judge_node → should_continue?
                                                            ├── Yes → advocate_node (loop)
                                                            └── No  → final_verdict → END
"""

from __future__ import annotations

from langgraph.graph import StateGraph, END

from debate_arena.graph.state import (
    DebateState,
    Argument,
    Verdict,
)
from debate_arena.agents import AdvocateAgent, OpponentAgent, JudgeAgent
from debate_arena.config import DebateConfig
from debate_arena.skills import read_skill
from debate_arena.tools.search import web_search
from debate_arena.tools.logic import logical_analysis


def build_debate_graph(config: DebateConfig | None = None) -> StateGraph:
    """Construct and compile the debate StateGraph.

    Args:
        config: Optional debate configuration.

    Returns:
        A compiled LangGraph that can be invoked with an initial DebateState.
    """
    config = config or DebateConfig()

    # ── Initialize agents ──
    advocate = AdvocateAgent(config)
    opponent = OpponentAgent(config)
    judge = JudgeAgent(config)

    # ── Define node functions ──

    def advocate_node(state: DebateState) -> dict:
        """Advocate presents an argument."""
        # Check for human-in-the-loop
        if config.human_role == "advocate":
            human_input = input("\n🎤 [You are the Advocate] Enter your argument:\n> ")
            content = human_input
        else:
            topic = state.get("topic", "")
            # Tool: fetch real web data
            web_results = web_search.invoke({"query": f"evidence supporting {topic}"})
            # Skill: read instructions on how to use the data
            skill_instructions = read_skill("research")
            context = f"{skill_instructions}\n\n## Web Search Results\n{web_results}"
            response = advocate.invoke(state, extra_context=context)
            raw = response.content
            content = " ".join(b.get("text", "") if isinstance(b, dict) else str(b) for b in raw) if isinstance(raw, list) else raw

        current_round = state.get("current_round", 0) + 1
        argument = Argument(
            role="advocate",
            round_number=current_round,
            content=content,
        )

        return {
            "advocate_arguments": [argument],
            "current_round": 1,  # Will be added by reducer
            "next_speaker": "opponent",
            "debate_status": "ongoing",
        }

    def opponent_node(state: DebateState) -> dict:
        """Opponent presents a counter-argument."""
        if config.human_role == "opponent":
            human_input = input("\n🎤 [You are the Opponent] Enter your argument:\n> ")
            content = human_input
        else:
            topic = state.get("topic", "")
            advocate_args = state.get("advocate_arguments", [])
            latest_adv = advocate_args[-1].content if advocate_args else ""
            # Tool: fetch counter-evidence from web
            web_results = web_search.invoke({"query": f"evidence against {topic}"})
            # Tool: analyze opponent's argument for logical fallacies
            fallacy_report = logical_analysis.invoke({"argument": latest_adv}) if latest_adv else ""
            # Skill: read instructions on how to rebut effectively
            research_instructions = read_skill("research")
            rebuttal_instructions = read_skill("rebuttal")
            context = (
                f"{research_instructions}\n\n"
                f"{rebuttal_instructions}\n\n"
                f"## Web Search Results (Counter-Evidence)\n{web_results}\n\n"
                + (f"## Logical Fallacy Analysis of Opponent's Argument\n{fallacy_report}" if fallacy_report else "")
            )
            response = opponent.invoke(state, extra_context=context)
            raw = response.content
            content = " ".join(b.get("text", "") if isinstance(b, dict) else str(b) for b in raw) if isinstance(raw, list) else raw

        current_round = state.get("current_round", 1)
        argument = Argument(
            role="opponent",
            round_number=current_round,
            content=content,
        )

        return {
            "opponent_arguments": [argument],
            "next_speaker": "judge",
        }

    def judge_node(state: DebateState) -> dict:
        """Judge evaluates the round and decides whether to continue."""
        round_result = judge.score_round(state)

        return {
            "round_results": [round_result],
            "debate_status": "concluded" if round_result.decision == "conclude" else "ongoing",
            "next_speaker": "advocate",
        }

    def final_verdict_node(state: DebateState) -> dict:
        """Produce the final debate verdict."""
        round_results = state.get("round_results", [])

        total_adv = sum(r.advocate_score.total for r in round_results)
        total_opp = sum(r.opponent_score.total for r in round_results)

        if total_adv > total_opp:
            winner = "advocate"
        elif total_opp > total_adv:
            winner = "opponent"
        else:
            winner = "draw"

        # Build summary
        summary_lines = [f"## Debate Verdict: {winner.upper()} wins!\n"]
        summary_lines.append(f"**Final Score**: Advocate {total_adv} vs Opponent {total_opp}\n")
        summary_lines.append("### Round-by-Round Breakdown")
        for r in round_results:
            summary_lines.append(
                f"- **Round {r.round_number}**: "
                f"Advocate {r.advocate_score.total} vs Opponent {r.opponent_score.total}"
            )
        summary_lines.append(f"\n### Judge's Notes")
        for r in round_results:
            summary_lines.append(f"**Round {r.round_number}**: {r.judge_feedback}")

        verdict = Verdict(
            winner=winner,
            summary="\n".join(summary_lines),
            total_advocate_score=total_adv,
            total_opponent_score=total_opp,
        )

        return {
            "verdict": verdict,
            "debate_status": "concluded",
        }

    # ── Conditional edge: should the debate continue? ──

    def should_continue(state: DebateState) -> str:
        """Route to next round or final verdict."""
        status = state.get("debate_status", "ongoing")
        if status == "concluded":
            return "final_verdict"
        return "advocate"

    # ── Build the graph ──

    graph = StateGraph(DebateState)

    # Add nodes
    graph.add_node("advocate", advocate_node)
    graph.add_node("opponent", opponent_node)
    graph.add_node("judge", judge_node)
    graph.add_node("final_verdict", final_verdict_node)

    # Add edges
    graph.set_entry_point("advocate")
    graph.add_edge("advocate", "opponent")
    graph.add_edge("opponent", "judge")
    graph.add_conditional_edges(
        "judge",
        should_continue,
        {
            "advocate": "advocate",       # Continue → next round
            "final_verdict": "final_verdict",  # Conclude → verdict
        },
    )
    graph.add_edge("final_verdict", END)

    return graph.compile()
