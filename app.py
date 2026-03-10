"""Streamlit UI for DebateArena."""

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from debate_arena.config import DebateConfig
from debate_arena.graph import build_debate_graph

st.set_page_config(page_title="DebateArena", page_icon="⚡", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"], .stApp {
    background-color: #09090b !important;
    color: #fafafa !important;
    font-family: 'Inter', sans-serif !important;
}

/* Hide Streamlit chrome */
#MainMenu, header[data-testid="stHeader"], footer,
div[data-testid="stToolbar"], div[data-testid="stDecoration"],
div[data-testid="stStatusWidget"] { display: none !important; }
.block-container { padding-top: 2rem !important; max-width: 1000px; }

/* Headings */
h1,h2,h3,h4 { font-family: 'Inter', sans-serif !important; color: #fafafa !important; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #111113 !important;
    border-right: 1px solid #27272a !important;
}
section[data-testid="stSidebar"] * { color: #d4d4d8 !important; }
section[data-testid="stSidebar"] label {
    font-size: 11px !important; font-weight: 600 !important;
    letter-spacing: 0.08em !important; text-transform: uppercase !important;
    color: #71717a !important;
}

/* Inputs */
.stTextInput input {
    background: #18181b !important;
    border: 1px solid #3f3f46 !important;
    border-radius: 8px !important;
    color: #fafafa !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
}
.stTextInput input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px #6366f130 !important;
    outline: none !important;
}
.stTextInput input::placeholder { color: #52525b !important; }

/* Select */
div[data-baseweb="select"] * {
    background: #18181b !important;
    border-color: #3f3f46 !important;
    color: #fafafa !important;
    font-family: 'Inter', sans-serif !important;
}
div[data-baseweb="popover"] { background: #18181b !important; border: 1px solid #3f3f46 !important; border-radius: 8px !important; }
div[data-baseweb="popover"] li { color: #fafafa !important; }
div[data-baseweb="popover"] li:hover { background: #27272a !important; }

/* All buttons */
.stButton > button {
    background: #18181b !important;
    border: 1px solid #3f3f46 !important;
    border-radius: 8px !important;
    color: #d4d4d8 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    transition: all 0.15s ease !important;
}
.stButton > button:hover {
    background: #27272a !important;
    border-color: #52525b !important;
    color: #fafafa !important;
}

/* Slider */
.stSlider [data-baseweb="slider"] div[role="slider"] { background: #6366f1 !important; }
.stSlider p, .stSlider span { color: #a1a1aa !important; font-size: 13px !important; }

/* Progress bar */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #6366f1, #8b5cf6) !important;
    border-radius: 99px !important;
}
.stProgress > div > div { background: #27272a !important; border-radius: 99px !important; }

/* Expanders */
details {
    background: #111113 !important;
    border: 1px solid #27272a !important;
    border-radius: 12px !important;
    margin-bottom: 12px !important;
    overflow: hidden !important;
}
details summary {
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    color: #a1a1aa !important;
    padding: 12px 16px !important;
    letter-spacing: 0 !important;
}
details[open] summary { color: #fafafa !important; }
details > div { padding: 0 4px 4px !important; }

/* Metrics */
div[data-testid="metric-container"] {
    background: #111113 !important;
    border: 1px solid #27272a !important;
    border-radius: 12px !important;
    padding: 20px !important;
}
div[data-testid="metric-container"] label {
    font-size: 11px !important; font-weight: 600 !important;
    text-transform: uppercase !important; letter-spacing: 0.08em !important;
    color: #71717a !important;
}
div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    font-size: 2.2rem !important; font-weight: 700 !important; color: #fafafa !important;
}

/* Markdown */
.stMarkdown p, .stMarkdown li { color: #d4d4d8 !important; line-height: 1.7 !important; }
.stMarkdown strong { color: #fafafa !important; }

/* Alerts */
div[data-testid="stAlert"] { background: #18181b !important; border-radius: 8px !important; color: #d4d4d8 !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 4px; background: #09090b; }
::-webkit-scrollbar-thumb { background: #27272a; border-radius: 99px; }
</style>
""", unsafe_allow_html=True)

# ── Header ──
st.markdown("""
<div style="margin-bottom: 32px; padding-bottom: 24px; border-bottom: 1px solid #27272a;">
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
        <div style="width: 8px; height: 8px; border-radius: 50%; background: #6366f1;
                    box-shadow: 0 0 8px #6366f1;"></div>
        <span style="font-size: 12px; font-weight: 500; color: #71717a; letter-spacing: 0.05em;">
            MULTI-AGENT AI SYSTEM
        </span>
    </div>
    <h1 style="font-size: 2.4rem; font-weight: 700; margin: 0; letter-spacing: -0.02em; color: #fafafa;">
        Debate<span style="color: #6366f1;">Arena</span>
    </h1>
    <p style="color: #71717a; margin: 6px 0 0; font-size: 14px;">
        Two AI agents debate any topic. A third judges every round.
    </p>
</div>
""", unsafe_allow_html=True)

EXAMPLES = [
    "AI will replace most white-collar jobs within 10 years",
    "Universal Basic Income is necessary in the age of automation",
    "Social media does more harm than good to society",
    "Space exploration funding should be redirected to climate change",
    "Remote work is more productive than office work",
]

if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = ""
if "run_debate" not in st.session_state:
    st.session_state.run_debate = False

# ── Sidebar ──
with st.sidebar:
    st.markdown("""
    <p style="font-size: 11px; font-weight: 600; text-transform: uppercase;
              letter-spacing: 0.08em; color: #71717a; margin-bottom: 16px;">Parameters</p>
    """, unsafe_allow_html=True)
    max_rounds = st.slider("Rounds", 1, 5, 3)
    model = st.selectbox("Model", ["claude-sonnet-4-6", "claude-haiku-4-5-20251001"])
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7)

start_debate = st.session_state.run_debate

# ── Helpers ──

def extract_summary(content, max_len: int = 280) -> str:
    if isinstance(content, list):
        content = " ".join(
            block.get("text", "") if isinstance(block, dict) else str(block)
            for block in content
        )
    content = content or ""
    lines = [l.strip() for l in content.strip().splitlines() if l.strip()]
    summary = ""
    for line in lines:
        if line.startswith("#"):
            continue
        summary += " " + line
        if len(summary) >= max_len:
            break
    summary = summary.strip()
    if len(summary) > max_len:
        summary = summary[:max_len].rsplit(" ", 1)[0] + "…"
    return summary


def render_round_summary(round_num: int, adv_content: str, opp_content: str):
    st.markdown(f"""
    <p style="font-size: 12px; font-weight: 600; text-transform: uppercase;
              letter-spacing: 0.08em; color: #71717a; margin: 24px 0 12px;">
        Round {round_num} — Summary
    </p>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style="padding: 16px; border: 1px solid #166534; background: #052e16;
                    border-radius: 10px; font-size: 14px; line-height: 1.65;">
            <div style="font-size: 11px; font-weight: 600; text-transform: uppercase;
                        letter-spacing: 0.08em; color: #4ade80; margin-bottom: 10px;">
                Advocate · Pro
            </div>
            <div style="color: #bbf7d0;">{extract_summary(adv_content)}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="padding: 16px; border: 1px solid #991b1b; background: #2d0a0a;
                    border-radius: 10px; font-size: 14px; line-height: 1.65;">
            <div style="font-size: 11px; font-weight: 600; text-transform: uppercase;
                        letter-spacing: 0.08em; color: #f87171; margin-bottom: 10px;">
                Opponent · Con
            </div>
            <div style="color: #fecaca;">{extract_summary(opp_content)}</div>
        </div>
        """, unsafe_allow_html=True)


def render_score_bar(label: str, score, color: str, bg: str):
    pct = int(score.total / 30 * 100)
    st.markdown(f"""
    <div style="padding: 16px; background: {bg}; border-radius: 10px;">
        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 10px;">
            <span style="font-size: 12px; font-weight: 600; text-transform: uppercase;
                         letter-spacing: 0.08em; color: {color};">{label}</span>
            <span style="font-size: 28px; font-weight: 700; color: #fafafa; line-height: 1;">
                {score.total}<span style="font-size: 14px; color: #71717a; font-weight: 400;">/30</span>
            </span>
        </div>
        <div style="background: #09090b; height: 6px; border-radius: 99px; overflow: hidden; margin-bottom: 10px;">
            <div style="width: {pct}%; height: 100%; background: {color}; border-radius: 99px;"></div>
        </div>
        <div style="display: flex; gap: 16px; font-size: 12px; color: #71717a;">
            <span>Logic <b style="color:#a1a1aa;">{score.logic}</b></span>
            <span>Evidence <b style="color:#a1a1aa;">{score.evidence}</b></span>
            <span>Persuasion <b style="color:#a1a1aa;">{score.persuasion}</b></span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_argument_card(role: str, round_num: int, content: str):
    if role == "advocate":
        color, label, dot = "#4ade80", "Advocate", "#4ade80"
    else:
        color, label, dot = "#f87171", "Opponent", "#f87171"
    with st.expander(f"{label}  ·  Round {round_num}", expanded=True):
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
            <div style="width: 6px; height: 6px; border-radius: 50%; background: {dot};
                        box-shadow: 0 0 6px {dot};"></div>
            <span style="font-size: 11px; font-weight: 600; text-transform: uppercase;
                         letter-spacing: 0.08em; color: {color};">{label} · Round {round_num}</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(content)


def render_status(text: str, kind: str = "info"):
    palette = {
        "info":    ("#818cf8", "#1e1b4b", "#3730a3"),
        "success": ("#4ade80", "#052e16", "#166534"),
        "error":   ("#f87171", "#2d0a0a", "#991b1b"),
        "warning": ("#fbbf24", "#1c1400", "#854d0e"),
    }
    fg, bg, border = palette.get(kind, palette["info"])
    st.markdown(f"""
    <div style="padding: 12px 16px; background: {bg}; border: 1px solid {border};
                border-radius: 8px; margin-bottom: 12px; font-size: 13px;
                font-weight: 500; color: {fg}; display: flex; align-items: center; gap: 8px;">
        <div style="width: 6px; height: 6px; border-radius: 50%;
                    background: {fg}; flex-shrink: 0;"></div>
        {text}
    </div>
    """, unsafe_allow_html=True)


# ── Main debate flow ──
if start_debate:
    topic = st.session_state.selected_topic
    st.session_state.run_debate = False
    config = DebateConfig(max_rounds=max_rounds, model_name=model, temperature=temperature)
    graph = build_debate_graph(config)

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

    st.markdown(f"""
    <div style="padding: 14px 18px; background: #18181b; border: 1px solid #27272a;
                border-radius: 10px; margin-bottom: 20px;">
        <span style="font-size: 11px; font-weight: 600; text-transform: uppercase;
                     letter-spacing: 0.08em; color: #71717a;">Topic</span>
        <p style="margin: 4px 0 0; font-size: 15px; font-weight: 500; color: #fafafa;">{topic}</p>
    </div>
    """, unsafe_allow_html=True)

    progress = st.progress(0)
    status_placeholder = st.empty()
    prev_adv = prev_opp = prev_rounds = 0

    for step in graph.stream(initial_state, stream_mode="values"):
        adv_args = step.get("advocate_arguments", [])
        for arg in adv_args[prev_adv:]:
            with status_placeholder:
                render_status(f"Round {arg.round_number}/{max_rounds} — Advocate is presenting...", "info")
            render_argument_card("advocate", arg.round_number, arg.content)
            progress.progress(min((arg.round_number - 0.66) / max_rounds, 0.95))
        prev_adv = len(adv_args)

        opp_args = step.get("opponent_arguments", [])
        for arg in opp_args[prev_opp:]:
            with status_placeholder:
                render_status(f"Round {arg.round_number}/{max_rounds} — Opponent is responding...", "error")
            render_argument_card("opponent", arg.round_number, arg.content)
            progress.progress(min((arg.round_number - 0.33) / max_rounds, 0.95))
        prev_opp = len(opp_args)

        rounds = step.get("round_results", [])
        for r in rounds[prev_rounds:]:
            adv_t, opp_t = r.advocate_score.total, r.opponent_score.total
            if adv_t > opp_t:
                msg, kind = f"Round {r.round_number} — Advocate leads  ({adv_t} vs {opp_t})", "success"
            elif opp_t > adv_t:
                msg, kind = f"Round {r.round_number} — Opponent leads  ({opp_t} vs {adv_t})", "error"
            else:
                msg, kind = f"Round {r.round_number} — Tied  ({adv_t} vs {opp_t})", "warning"
            with status_placeholder:
                render_status(msg, kind)

            adv_content = r.advocate_argument.content if r.advocate_argument else ""
            opp_content = r.opponent_argument.content if r.opponent_argument else ""
            if adv_content or opp_content:
                render_round_summary(r.round_number, adv_content, opp_content)

            with st.expander(f"Judge  ·  Round {r.round_number} Scoring", expanded=True):
                st.markdown(f"""
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 14px;">
                    <div style="width: 6px; height: 6px; border-radius: 50%; background: #a78bfa;
                                box-shadow: 0 0 6px #a78bfa;"></div>
                    <span style="font-size: 11px; font-weight: 600; text-transform: uppercase;
                                 letter-spacing: 0.08em; color: #a78bfa;">Judge · Round {r.round_number}</span>
                </div>
                <p style="color: #a1a1aa; font-size: 14px; line-height: 1.7;
                           border-left: 2px solid #3f3f46; padding-left: 14px; margin-bottom: 20px;">
                    {r.judge_feedback}
                </p>
                """, unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    render_score_bar("Advocate", r.advocate_score, "#4ade80", "#052e16")
                with col2:
                    render_score_bar("Opponent", r.opponent_score, "#f87171", "#2d0a0a")

            progress.progress(min(r.round_number / max_rounds, 0.95))
        prev_rounds = len(rounds)

        verdict = step.get("verdict")
        if verdict:
            progress.progress(1.0)
            status_placeholder.empty()

            wc = "#4ade80" if verdict.winner == "advocate" else (
                 "#f87171" if verdict.winner == "opponent" else "#818cf8")
            wb = "#052e16" if verdict.winner == "advocate" else (
                 "#2d0a0a" if verdict.winner == "opponent" else "#1e1b4b")

            st.markdown(f"""
            <div style="background: {wb}; border: 1px solid {wc}55; border-radius: 16px;
                        padding: 36px; margin: 28px 0; text-align: center;">
                <p style="font-size: 12px; font-weight: 600; text-transform: uppercase;
                           letter-spacing: 0.1em; color: {wc}99; margin: 0 0 8px;">Final Verdict</p>
                <h2 style="font-size: 3rem; font-weight: 700; letter-spacing: -0.02em;
                            color: {wc}; margin: 0 0 12px; line-height: 1;">
                    {verdict.winner.title()} Wins
                </h2>
                <p style="font-size: 14px; color: #71717a; margin: 0;">
                    Advocate {verdict.total_advocate_score} pts
                    &nbsp;·&nbsp;
                    Opponent {verdict.total_opponent_score} pts
                </p>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            col1.metric("Advocate Total", verdict.total_advocate_score)
            col2.metric("Opponent Total", verdict.total_opponent_score)

            st.markdown(f"""
            <div style="margin-top: 20px; padding: 24px; background: #111113;
                        border-radius: 12px; border: 1px solid #27272a;
                        font-size: 15px; line-height: 1.75; color: #a1a1aa;">
                <p style="font-size: 11px; font-weight: 600; text-transform: uppercase;
                           letter-spacing: 0.08em; color: #52525b; margin: 0 0 12px;">
                    Debate Summary
                </p>
                {verdict.summary}
            </div>
            """, unsafe_allow_html=True)

else:
    # ── Welcome ──
    st.markdown("""
    <style>
    div[data-testid="stTextInput"] input {
        font-size: 16px !important;
        padding: 14px 18px !important;
        border-radius: 10px !important;
    }
    .launch-btn > button {
        background: #6366f1 !important;
        border: none !important;
        color: #fff !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        padding: 14px !important;
        border-radius: 10px !important;
        letter-spacing: 0 !important;
    }
    .launch-btn > button:hover {
        background: #4f46e5 !important;
        box-shadow: 0 4px 20px #6366f140 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    _, center, _ = st.columns([1, 3, 1])
    with center:
        st.markdown("""
        <div style="text-align: center; margin: 32px 0 24px;">
            <h2 style="font-size: 1.6rem; font-weight: 700; letter-spacing: -0.02em;
                       color: #fafafa; margin: 0 0 8px;">What do you want to debate?</h2>
            <p style="font-size: 14px; color: #71717a; margin: 0;">
                Type any topic, or pick one below to get started instantly.
            </p>
        </div>
        """, unsafe_allow_html=True)

        typed = st.text_input(
            "topic",
            value=st.session_state.selected_topic,
            placeholder="e.g. Remote work is more productive than office work",
            label_visibility="collapsed",
        )
        st.markdown('<div class="launch-btn">', unsafe_allow_html=True)
        if st.button("Start Debate  →", use_container_width=True):
            st.session_state.selected_topic = typed
            st.session_state.run_debate = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
        <p style="font-size: 12px; font-weight: 600; text-transform: uppercase;
                   letter-spacing: 0.08em; color: #52525b; margin: 28px 0 10px;">
            Sample Topics
        </p>
        """, unsafe_allow_html=True)

        for ex in EXAMPLES:
            if st.button(ex, key=f"ex_{ex}", use_container_width=True):
                st.session_state.selected_topic = ex
                st.session_state.run_debate = True
                st.rerun()
