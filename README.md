# DebateArena

A multi-agent AI debate system where two Claude agents argue opposing sides of any topic, with a third agent judging each round in real-time.

Built with **LangGraph** + **LangChain Anthropic** + **Streamlit**.

---

## What it does

1. You enter a debate topic (or pick from examples)
2. The **Advocate** argues *for* the position
3. The **Opponent** argues *against* it
4. The **Judge** scores each round on Logic, Evidence, and Persuasion
5. After all rounds, a final verdict is rendered with a summary

Each agent uses web search (Tavily) to find real evidence before making arguments.

---

## Architecture

```
DebateArena
├── app.py                        # Streamlit UI
├── debate_arena/
│   ├── config.py                 # DebateConfig + system prompts
│   ├── agents/
│   │   ├── base.py               # Base agent (ChatAnthropic)
│   │   ├── advocate.py           # Argues FOR the topic
│   │   ├── opponent.py           # Argues AGAINST the topic
│   │   └── judge.py              # Scores and provides feedback
│   ├── graph/
│   │   ├── state.py              # DebateState (LangGraph TypedDict)
│   │   └── debate_graph.py       # StateGraph wiring + node logic
│   ├── tools/
│   │   ├── search.py             # web_search (Tavily)
│   │   ├── logic.py              # logical_analysis
│   │   └── citation.py           # cite_source
│   └── skills/
│       ├── research/SKILL.md     # How to use search results in arguments
│       └── rebuttal/SKILL.md     # How to construct rebuttals
└── test_core.py                  # Unit tests
```

### Tools vs Skills

Following the Claude Code / Agent SDK convention:
- **Tools** = executable Python functions decorated with `@tool` (search, logic, citation)
- **Skills** = `SKILL.md` instruction files read at runtime to guide agent behaviour

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Create `.env`

```bash
ANTHROPIC_API_KEY=sk-ant-...
TAVILY_API_KEY=tvly-...     # free tier at tavily.com
```

### 3. Run

```bash
streamlit run app.py
```

---

## Configuration

| Variable | Description | Required |
|---|---|---|
| `ANTHROPIC_API_KEY` | Claude API key | Yes |
| `TAVILY_API_KEY` | Web search API key | Yes |

Debate parameters (rounds, model, temperature) are adjustable in the sidebar.

---

## Models supported

| Model | Speed | Quality |
|---|---|---|
| `claude-sonnet-4-6` | Medium | Best |
| `claude-haiku-4-5-20251001` | Fast | Good |

---

## Scoring

Each argument is scored by the Judge on three dimensions (0–10 each):

| Dimension | What it measures |
|---|---|
| Logic | Coherence and soundness of reasoning |
| Evidence | Quality and relevance of supporting data |
| Persuasion | Rhetorical effectiveness |

Max score per round: **30 points per side**.

---

## License

MIT
