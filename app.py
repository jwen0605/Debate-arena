"""Streamlit UI for DebateArena – sci-fi HUD aesthetic."""

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from debate_arena.config import DebateConfig
from debate_arena.graph import build_debate_graph

# ── Page config ──
st.set_page_config(
    page_title="DebateArena",
    page_icon="⚡",
    layout="wide",
)

# ──────────────────────────────────────────────
# Color tokens  (edit here to retheme everything)
# BG: #1e1e2e  SURFACE: #2a2b3d  BORDER: #45465a
# TEXT: #e2e8f4  MUTED: #8891a8
# CYAN: #22d3ee  GREEN: #4ade80  RED: #f87171  PURPLE: #a78bfa
# ──────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@500;700&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"], .stApp {
    background-color: #1e1e2e !important;
    color: #e2e8f4 !important;
    font-family: 'Rajdhani', sans-serif !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, header[data-testid="stHeader"], footer,
div[data-testid="stToolbar"], div[data-testid="stDecoration"],
div[data-testid="stStatusWidget"] {
    display: none !important; height: 0 !important;
}
.block-container { padding-top: 1.5rem !important; max-width: 1100px; }

/* ── Headings ── */
h1, h2, h3, h4 {
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 700 !important;
    color: #e2e8f4 !important;
    letter-spacing: 2px !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #181825 !important;
    border-right: 1px solid #45465a !important;
}
section[data-testid="stSidebar"] * { color: #cdd0e4 !important; }
section[data-testid="stSidebar"] label {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 2px !important;
    color: #8891a8 !important;
}

/* ── Text inputs ── */
.stTextInput input, div[data-baseweb="select"] * {
    background: #2a2b3d !important;
    border: 1px solid #45465a !important;
    color: #e2e8f4 !important;
    border-radius: 4px !important;
    font-size: 14px !important;
}
.stTextInput input:focus {
    border-color: #22d3ee !important;
    box-shadow: 0 0 0 2px #22d3ee22 !important;
}

/* ── Select dropdown ── */
div[data-baseweb="popover"] {
    background: #2a2b3d !important;
    border: 1px solid #45465a !important;
}
div[data-baseweb="popover"] li { color: #e2e8f4 !important; background: transparent !important; }
div[data-baseweb="popover"] li:hover { background: #22d3ee18 !important; }

/* ── Primary button ── */
.stButton > button[kind="primary"] {
    background: #22d3ee18 !important;
    border: 1px solid #22d3ee !important;
    color: #22d3ee !important;
    font-family: 'Share Tech Mono', monospace !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    border-radius: 4px !important;
    font-size: 13px !important;
    transition: all 0.2s !important;
}
.stButton > button[kind="primary"]:hover {
    background: #22d3ee30 !important;
    box-shadow: 0 0 16px #22d3ee44 !important;
}

/* ── Slider ── */
.stSlider [data-baseweb="slider"] div[role="slider"] { background: #22d3ee !important; }
.stSlider p, .stSlider span { color: #cdd0e4 !important; font-size: 13px !important; }
div[data-testid="stSlider"] label { font-size: 11px !important; }

/* ── Progress ── */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #22d3ee, #a78bfa) !important;
    box-shadow: 0 0 6px #22d3ee88 !important;
}
.stProgress > div > div { background: #2a2b3d !important; border-radius: 4px !important; }

/* ── Expanders ── */
details {
    background: #2a2b3d !important;
    border: 1px solid #45465a !important;
    border-radius: 6px !important;
    margin-bottom: 10px !important;
}
details summary {
    color: #cdd0e4 !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 12px !important;
    letter-spacing: 1px !important;
    padding: 10px 14px !important;
}
details > div { color: #e2e8f4 !important; }

/* ── Alerts ── */
div[data-testid="stAlert"] {
    background: #2a2b3d !important;
    border-radius: 4px !important;
    color: #e2e8f4 !important;
}

/* ── Metrics ── */
div[data-testid="metric-container"] {
    background: #2a2b3d !important;
    border: 1px solid #45465a !important;
    border-radius: 6px !important;
    padding: 16px !important;
}
div[data-testid="metric-container"] label {
    color: #8891a8 !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 2px !important;
}
div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    color: #22d3ee !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 2.2rem !important;
    font-weight: 700 !important;
}

/* ── Markdown body text inside expanders / cards ── */
.stMarkdown p, .stMarkdown li, .stMarkdown span { color: #e2e8f4 !important; }
.stMarkdown strong { color: #f0f4ff !important; }

/* ── All buttons (default) ── */
.stButton > button {
    background: #2a2b3d !important;
    border: 1px solid #45465a !important;
    color: #f0f4ff !important;
    border-radius: 6px !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 13px !important;
    transition: all 0.15s ease !important;
}
.stButton > button:hover {
    border-color: #22d3ee !important;
    color: #22d3ee !important;
    background: #22d3ee12 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; background: #1e1e2e; }
::-webkit-scrollbar-thumb { background: #45465a; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ── Header ──
st.markdown("""
<div style="border-bottom: 1px solid #45465a; padding-bottom: 14px; margin-bottom: 24px;
            display: flex; align-items: flex-end; justify-content: space-between;">
    <div>
        <div style="font-family: 'Share Tech Mono', monospace; color: #22d3ee; font-size: 11px;
                    letter-spacing: 4px; margin-bottom: 4px;">AUTONOMOUS INTELLIGENCE SYSTEM</div>
        <h1 style="font-family: 'Rajdhani', sans-serif; font-weight: 700; font-size: 2.8rem;
                   letter-spacing: 6px; margin: 0; color: #e2e8f4; line-height: 1;">
            DEBATE<span style="color: #22d3ee;">ARENA</span>
        </h1>
    </div>
    <div style="font-family: 'Share Tech Mono', monospace; color: #8891a8; font-size: 11px;
                letter-spacing: 2px; text-align: right; padding-bottom: 4px;">
        MULTI-AGENT DEBATE<br>POWERED BY LANGGRAPH
    </div>
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

# ── Sidebar (parameters only) ──
with st.sidebar:
    st.markdown("""
    <div style="font-family: 'Share Tech Mono', monospace; color: #22d3ee; font-size: 11px;
                letter-spacing: 3px; margin-bottom: 20px; padding-bottom: 10px;
                border-bottom: 1px solid #45465a;">// PARAMETERS</div>
    """, unsafe_allow_html=True)
    max_rounds = st.slider("ROUNDS", 1, 5, 3)
    model = st.selectbox("MODEL", ["claude-sonnet-4-6", "claude-haiku-4-5-20251001"])
    temperature = st.slider("TEMPERATURE", 0.0, 1.0, 0.7)

# topic is set in the main area below
if "topic_input" not in st.session_state:
    st.session_state.topic_input = st.session_state.selected_topic

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
    <div style="font-family: 'Share Tech Mono', monospace; font-size: 11px;
                letter-spacing: 2px; color: #8891a8; margin: 20px 0 10px;">
        ── ROUND {round_num} SUMMARY ──
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style="padding: 16px; border: 1px solid #4ade8055; background: #4ade8010;
                    border-radius: 6px; font-size: 14px; line-height: 1.65;">
            <div style="font-family: 'Share Tech Mono', monospace; font-size: 10px;
                        letter-spacing: 3px; color: #4ade80; margin-bottom: 10px; font-weight: 600;">
                ADVOCATE // PRO
            </div>
            <div style="color: #d4edda;">{extract_summary(adv_content)}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="padding: 16px; border: 1px solid #f8717155; background: #f8717110;
                    border-radius: 6px; font-size: 14px; line-height: 1.65;">
            <div style="font-family: 'Share Tech Mono', monospace; font-size: 10px;
                        letter-spacing: 3px; color: #f87171; margin-bottom: 10px; font-weight: 600;">
                OPPONENT // CON
            </div>
            <div style="color: #fde8e8;">{extract_summary(opp_content)}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)


def render_score_bar(label: str, score, color: str):
    pct = int(score.total / 30 * 100)
    st.markdown(f"""
    <div style="margin-bottom: 14px;">
        <div style="display: flex; justify-content: space-between; align-items: baseline;
                    margin-bottom: 8px;">
            <span style="font-family: 'Share Tech Mono', monospace; color: {color};
                         font-size: 12px; letter-spacing: 2px;">{label}</span>
            <span style="color: {color}; font-family: 'Rajdhani', sans-serif;
                         font-size: 22px; font-weight: 700; line-height: 1;">
                {score.total}
                <span style="font-size: 13px; color: #8891a8; font-weight: 400;">/30</span>
            </span>
        </div>
        <div style="background: #1e1e2e; height: 6px; border-radius: 4px; overflow: hidden;">
            <div style="width: {pct}%; height: 100%; background: {color};
                        box-shadow: 0 0 6px {color}88;"></div>
        </div>
        <div style="display: flex; gap: 20px; margin-top: 8px;
                    font-family: 'Share Tech Mono', monospace; font-size: 11px; color: #8891a8;">
            <span>LOGIC&nbsp;<b style="color:#cdd0e4;">{score.logic}</b></span>
            <span>EVIDENCE&nbsp;<b style="color:#cdd0e4;">{score.evidence}</b></span>
            <span>PERSUASION&nbsp;<b style="color:#cdd0e4;">{score.persuasion}</b></span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_argument_card(role: str, round_num: int, content: str):
    if role == "advocate":
        color, label = "#4ade80", "ADVOCATE"
    else:
        color, label = "#f87171", "OPPONENT"
    with st.expander(f"{label}  ·  ROUND {round_num}", expanded=True):
        st.markdown(f"""
        <div style="border-left: 3px solid {color}; padding-left: 14px; margin-bottom: 10px;">
            <span style="font-family: 'Share Tech Mono', monospace; font-size: 10px;
                         letter-spacing: 3px; color: {color};">{label} // ROUND {round_num}</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(content)


def render_status(text: str, kind: str = "info"):
    palette = {
        "info":    ("#22d3ee", "#22d3ee18", "#22d3ee55"),
        "success": ("#4ade80", "#4ade8018", "#4ade8055"),
        "error":   ("#f87171", "#f8717118", "#f8717155"),
        "warning": ("#fbbf24", "#fbbf2418", "#fbbf2455"),
    }
    fg, bg, border = palette.get(kind, palette["info"])
    st.markdown(f"""
    <div style="padding: 10px 16px; border: 1px solid {border}; background: {bg};
                border-radius: 4px; margin-bottom: 10px;
                font-family: 'Share Tech Mono', monospace; font-size: 12px;
                letter-spacing: 1px; color: {fg};">
        ▶ {text}
    </div>
    """, unsafe_allow_html=True)


# ── Main debate flow ──
if start_debate:
    topic = st.session_state.selected_topic
    st.session_state.run_debate = False
    config = DebateConfig(
        max_rounds=max_rounds,
        model_name=model,
        temperature=temperature,
    )
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

    # Show the active topic
    st.markdown(f"""
    <div style="padding: 12px 18px; background: #2a2b3d; border: 1px solid #45465a;
                border-radius: 6px; margin-bottom: 20px;
                font-family: 'Share Tech Mono', monospace; font-size: 13px; color: #cdd0e4;">
        <span style="color: #8891a8; letter-spacing: 2px; font-size: 10px;">TOPIC </span>
        &nbsp;{topic}
    </div>
    """, unsafe_allow_html=True)

    progress = st.progress(0)
    status_placeholder = st.empty()
    prev_adv = prev_opp = prev_rounds = 0

    for step in graph.stream(initial_state, stream_mode="values"):
        adv_args = step.get("advocate_arguments", [])
        for arg in adv_args[prev_adv:]:
            with status_placeholder:
                render_status(f"ROUND {arg.round_number}/{max_rounds}  //  ADVOCATE TRANSMITTING...", "info")
            render_argument_card("advocate", arg.round_number, arg.content)
            progress.progress(min((arg.round_number - 0.66) / max_rounds, 0.95))
        prev_adv = len(adv_args)

        opp_args = step.get("opponent_arguments", [])
        for arg in opp_args[prev_opp:]:
            with status_placeholder:
                render_status(f"ROUND {arg.round_number}/{max_rounds}  //  OPPONENT RESPONDING...", "error")
            render_argument_card("opponent", arg.round_number, arg.content)
            progress.progress(min((arg.round_number - 0.33) / max_rounds, 0.95))
        prev_opp = len(opp_args)

        rounds = step.get("round_results", [])
        for r in rounds[prev_rounds:]:
            adv_t, opp_t = r.advocate_score.total, r.opponent_score.total
            if adv_t > opp_t:
                msg, kind = f"ROUND {r.round_number} COMPLETE  //  ADVOCATE LEADS  [{adv_t} vs {opp_t}]", "success"
            elif opp_t > adv_t:
                msg, kind = f"ROUND {r.round_number} COMPLETE  //  OPPONENT LEADS  [{opp_t} vs {adv_t}]", "error"
            else:
                msg, kind = f"ROUND {r.round_number} COMPLETE  //  TIED  [{adv_t} vs {opp_t}]", "warning"
            with status_placeholder:
                render_status(msg, kind)

            adv_content = r.advocate_argument.content if r.advocate_argument else ""
            opp_content = r.opponent_argument.content if r.opponent_argument else ""
            if adv_content or opp_content:
                render_round_summary(r.round_number, adv_content, opp_content)

            with st.expander(f"JUDGE  ·  ROUND {r.round_number} SCORING", expanded=True):
                st.markdown(f"""
                <div style="font-family: 'Share Tech Mono', monospace; font-size: 10px;
                            letter-spacing: 3px; color: #a78bfa; margin-bottom: 10px;">
                    ARBITER // ROUND {r.round_number}
                </div>
                <div style="border-left: 3px solid #a78bfa55; padding-left: 14px;
                            color: #cdd0e4; font-size: 14px; line-height: 1.7; margin-bottom: 16px;">
                    {r.judge_feedback}
                </div>
                """, unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    render_score_bar("ADVOCATE", r.advocate_score, "#4ade80")
                with col2:
                    render_score_bar("OPPONENT", r.opponent_score, "#f87171")

            progress.progress(min(r.round_number / max_rounds, 0.95))
        prev_rounds = len(rounds)

        verdict = step.get("verdict")
        if verdict:
            progress.progress(1.0)
            status_placeholder.empty()

            wc = "#4ade80" if verdict.winner == "advocate" else (
                 "#f87171" if verdict.winner == "opponent" else "#22d3ee")

            st.markdown(f"""
            <div style="border: 1px solid {wc}55; background: {wc}0d; border-radius: 8px;
                        padding: 32px; margin: 24px 0; text-align: center;">
                <div style="font-family: 'Share Tech Mono', monospace; font-size: 11px;
                            letter-spacing: 4px; color: {wc}99; margin-bottom: 10px;">
                    FINAL VERDICT
                </div>
                <div style="font-family: 'Rajdhani', sans-serif; font-weight: 700;
                            font-size: 3rem; letter-spacing: 6px; color: {wc}; line-height: 1;">
                    {verdict.winner.upper()} WINS
                </div>
                <div style="font-family: 'Share Tech Mono', monospace; font-size: 13px;
                            color: #8891a8; margin-top: 12px; letter-spacing: 1px;">
                    ADVOCATE {verdict.total_advocate_score} pts
                    &nbsp;&nbsp;·&nbsp;&nbsp;
                    OPPONENT {verdict.total_opponent_score} pts
                </div>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            col1.metric("ADVOCATE TOTAL", verdict.total_advocate_score)
            col2.metric("OPPONENT TOTAL", verdict.total_opponent_score)

            st.markdown(f"""
            <div style="margin-top: 20px; padding: 20px 24px; background: #2a2b3d;
                        border-radius: 6px; border: 1px solid #45465a;
                        font-size: 15px; line-height: 1.75; color: #cdd0e4;">
                <div style="font-family: 'Share Tech Mono', monospace; font-size: 10px;
                            letter-spacing: 3px; color: #8891a8; margin-bottom: 12px;">
                    // DEBATE SUMMARY
                </div>
                {verdict.summary}
            </div>
            """, unsafe_allow_html=True)

else:
    # ── Welcome: centered topic input ──
    st.markdown("""
    <style>
    /* Large centered topic input */
    div[data-testid="stTextInput"] input {
        font-size: 17px !important;
        padding: 14px 18px !important;
        height: auto !important;
    }
    /* Launch button */
    .launch-btn > button {
        background: #22d3ee20 !important;
        border: 1px solid #22d3ee !important;
        color: #22d3ee !important;
        font-size: 15px !important;
        letter-spacing: 4px !important;
        padding: 14px !important;
        border-radius: 6px !important;
    }
    .launch-btn > button:hover {
        background: #22d3ee35 !important;
        box-shadow: 0 0 20px #22d3ee44 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    _, center, _ = st.columns([1, 3, 1])
    with center:
        st.markdown("""
        <div style="margin: 32px 0 10px; text-align: center;">
            <div style="font-family: 'Rajdhani', sans-serif; font-size: 22px; font-weight: 700;
                        color: #e2e8f4; letter-spacing: 3px; margin-bottom: 6px;">
                What do you want to debate today?
            </div>
            <div style="font-family: 'Share Tech Mono', monospace; font-size: 11px;
                        color: #8891a8; letter-spacing: 2px;">
                Type your topic below, or pick one from the list
            </div>
        </div>
        """, unsafe_allow_html=True)
        typed = st.text_input(
            "topic",
            value=st.session_state.selected_topic,
            placeholder="e.g. AI will replace most white-collar jobs within 10 years",
            label_visibility="collapsed",
        )
        st.markdown("<div style='height: 8px'></div>", unsafe_allow_html=True)
        st.markdown('<div class="launch-btn">', unsafe_allow_html=True)
        if st.button("⚡  INITIATE DEBATE", use_container_width=True):
            st.session_state.selected_topic = typed
            st.session_state.run_debate = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
        <div style="font-family: 'Share Tech Mono', monospace; font-size: 11px;
                    letter-spacing: 3px; color: #8891a8; margin: 28px 0 12px;">
            // SAMPLE TOPICS
        </div>
        """, unsafe_allow_html=True)

        for ex in EXAMPLES:
            if st.button(f"› {ex}", key=f"ex_{ex}", use_container_width=True):
                st.session_state.selected_topic = ex
                st.session_state.run_debate = True
                st.rerun()

