"""Skills are Markdown instruction files (SKILL.md) that guide agent behaviour.

Usage:
    from debate_arena.skills import read_skill
    instructions = read_skill("research")   # reads skills/research/SKILL.md
    instructions = read_skill("rebuttal")   # reads skills/rebuttal/SKILL.md
"""

from pathlib import Path


def read_skill(skill_name: str) -> str:
    """Read a SKILL.md file and return its contents as a string."""
    skill_path = Path(__file__).parent / skill_name / "SKILL.md"
    if not skill_path.exists():
        raise FileNotFoundError(f"Skill not found: {skill_path}")
    return skill_path.read_text()
