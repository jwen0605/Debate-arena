"""CLI entry point for DebateArena."""

from __future__ import annotations

import argparse

from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

from debate_arena.config import DebateConfig
from debate_arena.graph import build_debate_graph

console = Console()


def print_header(topic: str, max_rounds: int):
    console.print()
    console.print(
        Panel(
            f"[bold cyan]🏟️ DebateArena[/bold cyan]\n\n"
            f"[bold]Topic:[/bold] {topic}\n"
            f"[bold]Rounds:[/bold] {max_rounds}",
            title="Multi-Agent Debate",
            border_style="cyan",
        )
    )
    console.print()


def print_argument(role: str, round_num: int, content: str):
    color = "green" if role == "advocate" else "red"
    emoji = "✅" if role == "advocate" else "❌"
    console.print(
        Panel(
            Markdown(content),
            title=f"{emoji} {role.title()} – Round {round_num}",
            border_style=color,
        )
    )


def print_scores(round_result):
    table = Table(title=f"Round {round_result.round_number} Scores")
    table.add_column("Dimension", style="bold")
    table.add_column("Advocate", justify="center", style="green")
    table.add_column("Opponent", justify="center", style="red")

    adv = round_result.advocate_score
    opp = round_result.opponent_score
    for dim in ["logic", "evidence", "persuasion"]:
        table.add_row(dim.title(), str(getattr(adv, dim)), str(getattr(opp, dim)))
    table.add_row("TOTAL", f"[bold]{adv.total}[/bold]", f"[bold]{opp.total}[/bold]")

    console.print(table)
    console.print(f"\n[dim]Judge feedback:[/dim] {round_result.judge_feedback}\n")


def print_verdict(verdict):
    winner_color = {"advocate": "green", "opponent": "red", "draw": "yellow"}
    console.print()
    console.print(
        Panel(
            Markdown(verdict.summary),
            title=f"🏆 Final Verdict: {verdict.winner.upper()}",
            border_style=winner_color.get(verdict.winner, "white"),
        )
    )


def run_debate(topic: str, max_rounds: int = 3, human_role: str | None = None):
    """Run a full debate and stream results to the console."""
    config = DebateConfig(max_rounds=max_rounds, human_role=human_role)
    graph = build_debate_graph(config)

    print_header(topic, max_rounds)

    # Initial state
    initial_state = {
        "topic": topic,
        "max_rounds": max_rounds,
        "current_round": 0,
        "advocate_arguments": [],
        "opponent_arguments": [],
        "round_results": [],
        "debate_status": "opening",
        "next_speaker": "advocate",
        "verdict": None,
    }

    # Stream through the graph
    prev_adv_count = 0
    prev_opp_count = 0
    prev_round_count = 0

    for step in graph.stream(initial_state, stream_mode="values"):
        # Print new advocate arguments
        adv_args = step.get("advocate_arguments", [])
        for arg in adv_args[prev_adv_count:]:
            print_argument("advocate", arg.round_number, arg.content)
        prev_adv_count = len(adv_args)

        # Print new opponent arguments
        opp_args = step.get("opponent_arguments", [])
        for arg in opp_args[prev_opp_count:]:
            print_argument("opponent", arg.round_number, arg.content)
        prev_opp_count = len(opp_args)

        # Print new round results
        rounds = step.get("round_results", [])
        for r in rounds[prev_round_count:]:
            print_scores(r)
        prev_round_count = len(rounds)

        # Print verdict if available
        verdict = step.get("verdict")
        if verdict:
            print_verdict(verdict)


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="🏟️ DebateArena – Multi-Agent Debate System"
    )
    parser.add_argument(
        "--topic",
        type=str,
        required=True,
        help="The debate topic/proposition",
    )
    parser.add_argument(
        "--rounds",
        type=int,
        default=3,
        help="Maximum number of debate rounds (default: 3)",
    )
    parser.add_argument(
        "--human",
        type=str,
        choices=["advocate", "opponent"],
        default=None,
        help="Take over a role as a human participant",
    )
    args = parser.parse_args()

    run_debate(topic=args.topic, max_rounds=args.rounds, human_role=args.human)


if __name__ == "__main__":
    main()
