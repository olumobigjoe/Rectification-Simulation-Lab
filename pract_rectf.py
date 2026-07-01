import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import os

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Rectification for Beginners",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background: #0b0f1a; color: #e0e6f0; }

    .hero-banner {
        background: linear-gradient(135deg, #0d1b2a 0%, #11213a 50%, #0a1628 100%);
        border: 1px solid #1e3a5f; border-radius: 12px;
        padding: 28px 36px; margin-bottom: 24px;
        position: relative; overflow: hidden;
    }
    .hero-banner::before {
        content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
        background: linear-gradient(90deg, transparent, #00d4ff, #0080ff, transparent);
    }
    .hero-title    { font-family: 'Share Tech Mono', monospace; font-size: 2rem; color: #00d4ff; margin: 0; letter-spacing: 0.05em; }
    .hero-subtitle { font-size: 0.9rem; color: #7a9cc4; margin-top: 6px; letter-spacing: 0.08em; text-transform: uppercase; }

    .metric-card { background: #111827; border: 1px solid #1e3a5f; border-radius: 8px; padding: 14px 16px; text-align: center; }
    .metric-card .label { font-size: 0.7rem; color: #7a9cc4; text-transform: uppercase; letter-spacing: 0.1em; }
    .metric-card .value { font-family: 'Share Tech Mono', monospace; font-size: 1.5rem; color: #00d4ff; margin-top: 4px; }
    .metric-card .unit  { font-size: 0.7rem; color: #4a7a9b; }

    .param-display {
        background: #0d1520; border: 1px solid #1e3a5f; border-radius: 8px;
        padding: 10px 0; text-align: center;
        font-family: 'Share Tech Mono', monospace; font-size: 1.3rem; color: #00d4ff;
    }
    .param-label {
        font-size: 0.72rem; color: #7a9cc4; text-transform: uppercase;
        letter-spacing: 0.1em; text-align: center; margin-bottom: 4px;
    }

    .theory-box {
        background: #0d1b2a; border-left: 3px solid #0080ff;
        border-radius: 0 8px 8px 0; padding: 16px 20px; margin: 12px 0;
        font-size: 0.88rem; color: #c0d4e8; line-height: 1.65;
    }
    .theory-box strong { color: #00d4ff; }

    .section-header {
        font-family: 'Share Tech Mono', monospace; font-size: 0.8rem; color: #00d4ff;
        letter-spacing: 0.15em; text-transform: uppercase;
        border-bottom: 1px solid #1e3a5f; padding-bottom: 6px; margin: 20px 0 12px;
    }

    [data-testid="stSidebar"] { background: #0d1520; border-right: 1px solid #1e3a5f; }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: #00d4ff; }
    .stSelectbox label { color: #c0d4e8 !important; font-size: 0.85rem !important; }

    .stTabs [data-baseweb="tab-list"] { background: #0d1520; border-bottom: 1px solid #1e3a5f; gap: 2px; }
    .stTabs [data-baseweb="tab"] { background: transparent; color: #7a9cc4; border: none;
        font-size: 0.85rem; font-family: 'Share Tech Mono', monospace; letter-spacing: 0.05em; }
    .stTabs [aria-selected="true"] { background: #111827 !important; color: #00d4ff !important;
        border-bottom: 2px solid #00d4ff !important; }

    /* All buttons share base style; stepper buttons get overridden via key trick */
    .stButton > button {
        background: #0d2a4a; color: #00d4ff; border: 1px solid #0080ff; border-radius: 6px;
        font-family: 'Share Tech Mono', monospace; font-size: 0.8rem; letter-spacing: 0.05em;
        transition: all 0.2s; width: 100%;
    }
    .stButton > button:hover { background: #0f3d6e; border-color: #00d4ff; }
</style>
""", unsafe_allow_html=True)

# ─── ANALYTICS LOGGER ────────────────────────────────────────────────────────
LOG_FILE = "rectification_lab_log.csv"

def log_action(student_id, action, details=""):
    entry = pd.DataFrame([{
        "Timestamp":  datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Student_ID": student_id,
        "Action":     action,
        "Details":    str(details)
    }])
    if not os.path.isfile(LOG_FILE):
        entry.to_csv(LOG_FILE, index=False)
    else:
        entry.to_csv(LOG_FILE, mode='a', header=False, index=False)

# ─── SESSION STATE ────────────────────────────────────────────────────────────
defaults = {
    "auth":       False,
    "student_id": "",
    "Vp":         12.0,   # Peak voltage default
    "freq":       50,     # Frequency default
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─── HERO BANNER ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <p class="hero-title">⚡ TOPIC: Rectification</p>
    <p class="hero-subtitle">SIMULATION LABORATORY</p>
    <p class="hero-subtitle">Department of Physics/Electronics</p>
</div>
""", unsafe_allow_html=True)

# ─── LOGIN GATE ──────────────────────────────────────────────────────────────
if not st.session_state["auth"]:
    st.markdown('<p class="section-header">ACCESS</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.4, 1])
    with c2:
        st.markdown("Enter your **Matriculation Number**")
        matric = st.text_input("Matriculation Number", placeholder="e.g. PHY/2026/0001")
        if st.button("▶  LOGIN"):
            if matric.strip():
                st.session_state["student_id"] = matric.strip()
                st.session_state["auth"] = True
                log_action(matric.strip(), "Session_Start")
                st.rerun()
            else:
                st.error("Matriculation number is required.")
    st.stop()

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Circuit Parameters")

    mode = st.selectbox(
        "Rectifier Type",
        ["Half-Wave Rectifier", "Full-Wave — Centre Tap", "Full-Wave — Bridge"],
        help="Select the rectifier topology to simulate."
    )

    st.markdown("---")
    st.markdown("### AC Source")

    # ── Peak Voltage stepper ──────────────────────────────
    st.markdown('<p class="param-label">Peak Voltage  Vₚ</p>', unsafe_allow_html=True)
    vp_col1, vp_col2, vp_col3 = st.columns([1, 1.6, 1])
    with vp_col1:
        if st.button("−", key="vp_down"):
            st.session_state["Vp"] = max(1.0, round(st.session_state["Vp"] - 0.5, 1))
    with vp_col2:
        st.markdown(f'<div class="param-display">{st.session_state["Vp"]:.1f} V</div>',
                    unsafe_allow_html=True)
    with vp_col3:
        if st.button("+", key="vp_up"):
            st.session_state["Vp"] = min(50.0, round(st.session_state["Vp"] + 0.5, 1))

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Frequency stepper ────────────────────────────────
    st.markdown('<p class="param-label">Frequency  f</p>', unsafe_allow_html=True)
    fr_col1, fr_col2, fr_col3 = st.columns([1, 1.6, 1])
    with fr_col1:
        if st.button("−", key="fr_down"):
            st.session_state["freq"] = max(10, st.session_state["freq"] - 10)
    with fr_col2:
        st.markdown(f'<div class="param-display">{st.session_state["freq"]} Hz</div>',
                    unsafe_allow_html=True)
    with fr_col3:
        if st.button("+", key="fr_up"):
            st.session_state["freq"] = min(500, st.session_state["freq"] + 10)

    st.markdown("---")
    st.caption(f"👤 Student: `{st.session_state['student_id']}`")
    if st.button("🔒 Log Out"):
        st.session_state["auth"] = False
        st.rerun()

# ─── READ CURRENT VALUES FROM SESSION STATE ───────────────────────────────────
Vp   = st.session_state["Vp"]
freq = st.session_state["freq"]

# ─── FIXED CIRCUIT CONSTANTS ─────────────────────────────────────────────────
Vd       = 0.7
RL       = 500
n_cycles = 3

# ─── SIGNAL GENERATION ───────────────────────────────────────────────────────
T    = 1.0 / freq
t    = np.linspace(0, n_cycles * T, 8000)
v_in = Vp * np.sin(2 * np.pi * freq * t)

def half_wave(v, vd):
    return np.where(v > vd, v - vd, 0.0)

def full_wave_ct(v, vd):
    return np.where(np.abs(v) > vd, np.abs(v) - vd, 0.0)

def full_wave_bridge(v, vd):
    return np.where(np.abs(v) > 2 * vd, np.abs(v) - 2 * vd, 0.0)

# ─── TOPOLOGY ────────────────────────────────────────────────────────────────
if mode == "Half-Wave Rectifier":
    v_out            = half_wave(v_in, Vd)
    color_main       = "#4ade80"
    fill_main        = "rgba(74,222,128,0.08)"
    label_rect       = "Half-Wave Output"
    n_diodes         = 1
    ripple_freq_mult = 1
elif mode == "Full-Wave — Centre Tap":
    v_out            = full_wave_ct(v_in, Vd)
    color_main       = "#818cf8"
    fill_main        = "rgba(129,140,248,0.08)"
    label_rect       = "Full-Wave CT Output"
    n_diodes         = 2
    ripple_freq_mult = 2
else:
    v_out            = full_wave_bridge(v_in, Vd)
    color_main       = "#fb923c"
    fill_main        = "rgba(251,146,60,0.08)"
    label_rect       = "Bridge Rectifier Output"
    n_diodes         = 4
    ripple_freq_mult = 2

# ─── METRICS ─────────────────────────────────────────────────────────────────
Vout_peak     = float(v_out.max())
Vout_dc       = float(v_out.mean())
Vout_rms      = float(np.sqrt(np.mean(v_out ** 2)))
Vin_rms       = float(np.sqrt(np.mean(v_in  ** 2)))
Vripple_pp    = float(v_out.max() - v_out.min())
Vac_rms       = float(np.sqrt(max(Vout_rms**2 - Vout_dc**2, 0.0)))
ripple_factor = (Vac_rms / Vout_dc) if Vout_dc > 0 else 0.0
P_dc          = (Vout_dc**2)  / RL
P_in          = (Vin_rms**2)  / RL
eta           = (P_dc / P_in * 100) if P_in > 0 else 0.0
Idc           = Vout_dc   / RL * 1000
Ipeak         = Vout_peak / RL * 1000
PIV           = (2 * Vp - Vd) if mode == "Full-Wave — Centre Tap" else Vp

log_action(st.session_state["student_id"], "Signal_Generated",
           f"Mode={mode}, Vp={Vp}, f={freq}")

# ─── CIRCUIT DIAGRAM HTML TEMPLATES ──────────────────────────────────────────
# Rendered via components.html to bypass Streamlit's SVG sanitiser

DIAG_STYLE = """
<style>
  body { margin:0; padding:8px; background:#0d1520; }
  .w   { stroke:#60a5fa; stroke-width:2; fill:none; }
  .t   { fill:#c0d4e8; font-family:monospace; font-size:13px; }
</style>
"""

def diag_hw():
    return DIAG_STYLE + """
<svg viewBox="0 0 620 150" xmlns="http://www.w3.org/2000/svg" width="100%">
  <defs>
    <marker id="arr" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto">
      <path d="M0,0 L8,4 L0,8 Z" fill="#facc15"/>
    </marker>
  </defs>

  <!-- AC Source -->
  <circle cx="70" cy="75" r="32" class="w"/>
  <text x="70" y="70" text-anchor="middle" class="t" font-size="18">~</text>
  <text x="70" y="120" text-anchor="middle" style="fill:#00d4ff;font-family:monospace;font-size:11px">Vᵢₙ</text>
  <text x="70" y="134" text-anchor="middle" style="fill:#7a9cc4;font-family:monospace;font-size:9px">AC Source</text>

  <!-- Top wire: source → diode -->
  <line x1="102" y1="43" x2="220" y2="43" class="w"/>

  <!-- Diode symbol (anode left, cathode right) -->
  <polygon points="220,28 220,58 252,43" style="fill:#4ade80;stroke:#4ade80;stroke-width:1"/>
  <line x1="252" y1="27" x2="252" y2="59" style="stroke:#4ade80;stroke-width:3"/>
  <text x="236" y="20" text-anchor="middle" style="fill:#4ade80;font-family:monospace;font-size:12px;font-weight:bold">D</text>

  <!-- Wire: diode → resistor -->
  <line x1="252" y1="43" x2="360" y2="43" class="w"/>

  <!-- Load resistor -->
  <rect x="360" y="28" width="90" height="30" rx="4" style="fill:#1a2a1a;stroke:#4ade80;stroke-width:1.8"/>
  <text x="405" y="48" text-anchor="middle" style="fill:#4ade80;font-family:monospace;font-size:12px">Rₗ</text>
  <text x="405" y="73" text-anchor="middle" style="fill:#7a9cc4;font-family:monospace;font-size:9px">500 Ω</text>

  <!-- Wire: resistor → right node -->
  <line x1="450" y1="43" x2="530" y2="43" class="w"/>
  <line x1="530" y1="43" x2="530" y2="107" class="w"/>

  <!-- Bottom return wire -->
  <line x1="102" y1="107" x2="530" y2="107" class="w"/>

  <!-- Vout measurement indicator -->
  <line x1="500" y1="49" x2="500" y2="101" style="stroke:#facc15;stroke-width:1.8;stroke-dasharray:5,3"/>
  <line x1="495" y1="49"  x2="505" y2="49"  style="stroke:#facc15;stroke-width:2"/>
  <line x1="495" y1="101" x2="505" y2="101" style="stroke:#facc15;stroke-width:2"/>
  <text x="510" y="78" style="fill:#facc15;font-family:monospace;font-size:11px">Vₒᵤₜ</text>
</svg>"""

def diag_fwct():
    return DIAG_STYLE + """
<svg viewBox="0 0 660 220" xmlns="http://www.w3.org/2000/svg" width="100%">
  <!-- Transformer box -->
  <rect x="20" y="50" width="70" height="120" rx="5" style="fill:#0a1222;stroke:#60a5fa;stroke-width:1.8"/>
  <text x="55" y="105" text-anchor="middle" class="t" font-size="20">~</text>
  <text x="55" y="125" text-anchor="middle" class="t" font-size="9">Transformer</text>
  <!-- Primary taps -->
  <line x1="90" y1="75"  x2="110" y2="75"  class="w"/>
  <line x1="90" y1="145" x2="110" y2="145" class="w"/>
  <!-- Centre tap (dashed) -->
  <line x1="90" y1="110" x2="480" y2="110" style="stroke:#60a5fa;stroke-width:1.5;stroke-dasharray:5,4"/>
  <text x="112" y="107" style="fill:#7a9cc4;font-family:monospace;font-size:9px">CT (GND)</text>

  <!-- D1 — top diode (anode at left of top rail) -->
  <line x1="110" y1="75" x2="200" y2="75" class="w"/>
  <polygon points="200,62 200,88 232,75" style="fill:#818cf8;stroke:#818cf8;stroke-width:1"/>
  <line x1="232" y1="61" x2="232" y2="89" style="stroke:#818cf8;stroke-width:3"/>
  <text x="216" y="55" text-anchor="middle" style="fill:#818cf8;font-family:monospace;font-size:12px;font-weight:bold">D₁</text>

  <!-- D2 — bottom diode (anode at left of bottom rail) -->
  <line x1="110" y1="145" x2="200" y2="145" class="w"/>
  <polygon points="200,132 200,158 232,145" style="fill:#818cf8;stroke:#818cf8;stroke-width:1"/>
  <line x1="232" y1="131" x2="232" y2="159" style="stroke:#818cf8;stroke-width:3"/>
  <text x="216" y="172" text-anchor="middle" style="fill:#818cf8;font-family:monospace;font-size:12px;font-weight:bold">D₂</text>

  <!-- Both cathodes join at right node -->
  <line x1="232" y1="75"  x2="320" y2="75"  class="w"/>
  <line x1="232" y1="145" x2="320" y2="145" class="w"/>
  <line x1="320" y1="75"  x2="320" y2="95"  class="w"/>
  <line x1="320" y1="145" x2="320" y2="125" class="w"/>
  <line x1="320" y1="95"  x2="360" y2="95"  class="w"/>
  <line x1="320" y1="125" x2="360" y2="125" class="w"/>

  <!-- Load resistor -->
  <rect x="360" y="90" width="90" height="40" rx="4" style="fill:#1a1a2a;stroke:#818cf8;stroke-width:1.8"/>
  <text x="405" y="115" text-anchor="middle" style="fill:#818cf8;font-family:monospace;font-size:12px">Rₗ</text>
  <text x="405" y="145" text-anchor="middle" style="fill:#7a9cc4;font-family:monospace;font-size:9px">500 Ω</text>

  <!-- Wire from resistor to right side -->
  <line x1="450" y1="95"  x2="530" y2="95"  class="w"/>
  <line x1="450" y1="125" x2="480" y2="125" class="w"/>
  <line x1="480" y1="125" x2="480" y2="110" class="w"/>
  <line x1="480" y1="110" x2="530" y2="110" class="w"/>

  <!-- Vout -->
  <line x1="530" y1="95"  x2="530" y2="110" class="w"/>
  <line x1="510" y1="97"  x2="510" y2="108" style="stroke:#facc15;stroke-width:1.8;stroke-dasharray:4,3"/>
  <line x1="505" y1="97"  x2="515" y2="97"  style="stroke:#facc15;stroke-width:2"/>
  <line x1="505" y1="108" x2="515" y2="108" style="stroke:#facc15;stroke-width:2"/>
  <text x="538" y="105" style="fill:#facc15;font-family:monospace;font-size:11px">Vₒᵤₜ</text>
</svg>"""

def diag_bridge():
    return DIAG_STYLE + """
<svg viewBox="0 0 660 230" xmlns="http://www.w3.org/2000/svg" width="100%">
  <!-- AC Source -->
  <circle cx="70" cy="115" r="32" class="w"/>
  <text x="70" y="110" text-anchor="middle" class="t" font-size="18">~</text>
  <text x="70" y="160" text-anchor="middle" style="fill:#00d4ff;font-family:monospace;font-size:11px">Vᵢₙ</text>
  <text x="70" y="173" text-anchor="middle" style="fill:#7a9cc4;font-family:monospace;font-size:9px">AC Source</text>

  <!-- Wires from source to bridge input nodes -->
  <!-- Top input node at (210, 75) -->
  <line x1="102" y1="83"  x2="210" y2="83"  class="w"/>
  <!-- Bottom input node at (210, 155) -->
  <line x1="102" y1="147" x2="210" y2="147" class="w"/>

  <!-- Bridge nodes: L=(210,115) T=(300,55) R=(390,115) B=(300,175) -->
  <!-- Left node vertical connector -->
  <line x1="210" y1="83"  x2="210" y2="147" class="w"/>

  <!-- D1: L→T  (left to top-output) -->
  <line x1="210" y1="115" x2="240" y2="90"  class="w"/>
  <polygon points="240,90 256,78 248,100" style="fill:#fb923c;stroke:#fb923c;stroke-width:1"/>
  <line x1="256" y1="68" x2="256" y2="88" style="stroke:#fb923c;stroke-width:3"/>
  <line x1="256" y1="78" x2="300" y2="55" class="w"/>
  <text x="230" y="68" style="fill:#fb923c;font-family:monospace;font-size:11px;font-weight:bold">D₁</text>

  <!-- D3: T→R  (top to right) -->
  <line x1="300" y1="55" x2="344" y2="78" class="w"/>
  <polygon points="344,78 336,100 352,90" style="fill:#fb923c;stroke:#fb923c;stroke-width:1"/>
  <line x1="352" y1="70" x2="352" y2="90" style="stroke:#fb923c;stroke-width:3"/>
  <line x1="352" y1="80" x2="390" y2="115" class="w"/>
  <text x="344" y="60" style="fill:#fb923c;font-family:monospace;font-size:11px;font-weight:bold">D₃</text>

  <!-- D4: L→B  (left to bottom) -->
  <line x1="210" y1="115" x2="240" y2="140" class="w"/>
  <polygon points="240,140 256,152 248,130" style="fill:#fb923c;stroke:#fb923c;stroke-width:1"/>
  <line x1="256" y1="142" x2="256" y2="162" style="stroke:#fb923c;stroke-width:3"/>
  <line x1="256" y1="152" x2="300" y2="175" class="w"/>
  <text x="218" y="166" style="fill:#fb923c;font-family:monospace;font-size:11px;font-weight:bold">D₄</text>

  <!-- D2: B→R  (bottom to right) -->
  <line x1="300" y1="175" x2="344" y2="152" class="w"/>
  <polygon points="344,152 336,130 352,140" style="fill:#fb923c;stroke:#fb923c;stroke-width:1"/>
  <line x1="352" y1="130" x2="352" y2="150" style="stroke:#fb923c;stroke-width:3"/>
  <line x1="352" y1="140" x2="390" y2="115" class="w"/>
  <text x="344" y="178" style="fill:#fb923c;font-family:monospace;font-size:11px;font-weight:bold">D₂</text>

  <!-- Right node down to load positive -->
  <line x1="390" y1="115" x2="430" y2="115" class="w"/>

  <!-- Bottom return from source back through bridge bottom node -->
  <!-- source bottom → bridge bottom node -->
  <!-- The bottom input wire splits: one goes to D4 anode side (left node), already connected -->
  <!-- Ground/return: bridge bottom node (300,175) → down → right → load negative -->
  <line x1="300" y1="175" x2="300" y2="200" class="w"/>
  <line x1="300" y1="200" x2="510" y2="200" class="w"/>
  <line x1="510" y1="200" x2="510" y2="135" class="w"/>

  <!-- Load resistor (vertical) -->
  <rect x="430" y="95" width="80" height="40" rx="4" style="fill:#2a1a0a;stroke:#fb923c;stroke-width:1.8"/>
  <text x="470" y="120" text-anchor="middle" style="fill:#fb923c;font-family:monospace;font-size:12px">Rₗ</text>
  <line x1="510" y1="95"  x2="510" y2="115" class="w"/>

  <!-- Vout indicator -->
  <line x1="555" y1="97"  x2="555" y2="133" style="stroke:#facc15;stroke-width:1.8;stroke-dasharray:5,3"/>
  <line x1="549" y1="97"  x2="561" y2="97"  style="stroke:#facc15;stroke-width:2"/>
  <line x1="549" y1="133" x2="561" y2="133" style="stroke:#facc15;stroke-width:2"/>
  <text x="563" y="118" style="fill:#facc15;font-family:monospace;font-size:11px">Vₒᵤₜ</text>

  <!-- Connect load top to right node -->
  <line x1="430" y1="115" x2="430" y2="95" class="w"/>
</svg>"""

# ─── TABS ────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "📈  WAVEFORM ANALYSER",
    "📐  CIRCUIT THEORY",
    "📊  METRICS DASHBOARD",
])

# ══════════════════════════════════════════════════════════
# TAB 1 — WAVEFORM ANALYSER
# ══════════════════════════════════════════════════════════
with tab1:
    st.markdown('<p class="section-header">// Live Waveform Measurements</p>', unsafe_allow_html=True)

    def mcard(col, label, val, unit):
        col.markdown(f"""
        <div class="metric-card">
            <div class="label">{label}</div>
            <div class="value">{val}</div>
            <div class="unit">{unit}</div>
        </div>""", unsafe_allow_html=True)

    m1, m2, m3, m4, m5, m6 = st.columns(6)
    mcard(m1, "V_peak",        f"{Vout_peak:.2f}",    "V")
    mcard(m2, "V_DC",          f"{Vout_dc:.2f}",      "V")
    mcard(m3, "V_RMS",         f"{Vout_rms:.2f}",     "V")
    mcard(m4, "Ripple Factor", f"{ripple_factor:.4f}", "γ")
    mcard(m5, "Efficiency",    f"{eta:.1f}",           "%")
    mcard(m6, "PIV",           f"{PIV:.2f}",           "V")

    st.markdown("")
    t_ms = t * 1000

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=t_ms, y=v_in,
        name="AC Input  vᵢₙ(t)",
        line=dict(color="#60a5fa", width=1.5, dash="dot"),
        opacity=0.65
    ))
    fig.add_trace(go.Scatter(
        x=t_ms, y=v_out,
        name=label_rect,
        line=dict(color=color_main, width=2.5),
        fill="tozeroy",
        fillcolor=fill_main
    ))
    fig.add_trace(go.Scatter(
        x=[t_ms[0], t_ms[-1]],
        y=[Vout_dc, Vout_dc],
        name=f"V_DC = {Vout_dc:.2f} V",
        line=dict(color="#facc15", width=1.5, dash="dash"),
        mode="lines"
    ))
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0b0f1a",
        plot_bgcolor="#0d1520",
        font=dict(family="Share Tech Mono, monospace", color="#c0d4e8", size=11),
        legend=dict(orientation="h", y=-0.18, x=0,
                    bgcolor="rgba(0,0,0,0)", bordercolor="#1e3a5f"),
        margin=dict(l=10, r=10, t=30, b=10),
        height=480,
        xaxis=dict(title="Time (ms)", gridcolor="#1a2a3a",
                   zeroline=True, zerolinecolor="#1e3a5f"),
        yaxis=dict(title="Voltage (V)", gridcolor="#1a2a3a",
                   zeroline=True, zerolinecolor="#1e3a5f"),
    )
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("⬇️  Export Waveform Data"):
        export_df = pd.DataFrame({
            "Time (ms)":            np.round(t_ms, 4),
            "AC Input (V)":         np.round(v_in, 4),
            "Rectified Output (V)": np.round(v_out, 4),
        })
        st.download_button(
            "Download as CSV",
            data=export_df.to_csv(index=False),
            file_name=f"rectification_{mode.replace(' ', '_').lower()}.csv",
            mime="text/csv"
        )

# ══════════════════════════════════════════════════════════
# TAB 2 — CIRCUIT THEORY
# ══════════════════════════════════════════════════════════
with tab2:
    st.markdown('<p class="section-header">// Circuit Theory &amp; Operation</p>', unsafe_allow_html=True)

    if mode == "Half-Wave Rectifier":
        st.markdown("""
        <div class="theory-box">
        <strong>Half-Wave Rectifier</strong><br><br>
        A single diode is placed in series with the load resistor Rₗ. During the <strong>positive half-cycle</strong>
        of the AC input, the diode is forward-biased and conducts — voltage appears across the load.
        During the <strong>negative half-cycle</strong>, the diode is reverse-biased and blocks current,
        so the output is zero.<br><br>
        <strong>Key equations:</strong><br>
        &nbsp;&nbsp;• V_DC = Vₚ / π ≈ 0.318 Vₚ<br>
        &nbsp;&nbsp;• V_RMS = Vₚ / 2<br>
        &nbsp;&nbsp;• Ripple factor γ = 1.21 (without filter)<br>
        &nbsp;&nbsp;• Rectifier efficiency η = 40.6%<br>
        &nbsp;&nbsp;• PIV = Vₚ<br><br>
        Because only one half-cycle is used, this topology is the <em>least efficient</em> of the three.
        It is only suitable for very low power or signal applications.
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<p class="section-header">// Circuit Diagram</p>', unsafe_allow_html=True)
        components.html(diag_hw(), height=170, scrolling=False)

    elif mode == "Full-Wave — Centre Tap":
        st.markdown("""
        <div class="theory-box">
        <strong>Full-Wave Centre-Tap Rectifier</strong><br><br>
        This uses a <strong>centre-tapped transformer</strong> and two diodes. The centre tap serves as the
        ground reference. During the positive half-cycle, diode D₁ conducts; during the negative half-cycle,
        diode D₂ conducts. <em>Both half-cycles appear at the output</em>, doubling the ripple frequency.<br><br>
        <strong>Key equations:</strong><br>
        &nbsp;&nbsp;• V_DC = 2Vₚ / π ≈ 0.636 Vₚ<br>
        &nbsp;&nbsp;• V_RMS = Vₚ / √2<br>
        &nbsp;&nbsp;• Ripple factor γ = 0.482 (without filter)<br>
        &nbsp;&nbsp;• Rectifier efficiency η = 81.2%<br>
        &nbsp;&nbsp;• PIV = 2Vₚ − Vd (each diode blocks the full secondary voltage)<br><br>
        The high PIV requirement means diodes with a higher voltage rating are needed compared to
        the bridge circuit, which is a practical disadvantage.
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<p class="section-header">// Circuit Diagram</p>', unsafe_allow_html=True)
        components.html(diag_fwct(), height=240, scrolling=False)

    else:
        st.markdown("""
        <div class="theory-box">
        <strong>Full-Wave Bridge Rectifier</strong><br><br>
        Four diodes are arranged in a <strong>bridge configuration</strong>. No centre-tap transformer is needed.
        During the positive half-cycle, D₁ and D₃ conduct; during the negative half-cycle, D₂ and D₄ conduct.
        Current through the load always flows in the <em>same direction</em>.<br><br>
        <strong>Key equations:</strong><br>
        &nbsp;&nbsp;• V_DC = 2Vₚ / π ≈ 0.636 Vₚ  (but 2×Vd loss)<br>
        &nbsp;&nbsp;• V_RMS = Vₚ / √2<br>
        &nbsp;&nbsp;• Ripple factor γ = 0.482 (without filter)<br>
        &nbsp;&nbsp;• Rectifier efficiency η = 81.2%<br>
        &nbsp;&nbsp;• PIV = Vₚ − Vd (lower than centre-tap → cheaper diodes)<br><br>
        The bridge is the <em>most widely used</em> rectifier topology in power supplies because it does not
        require a centre-tap and has a lower PIV requirement per diode.
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<p class="section-header">// Circuit Diagram</p>', unsafe_allow_html=True)
        components.html(diag_bridge(), height=250, scrolling=False)

    st.markdown('<p class="section-header">// Comparative Summary</p>', unsafe_allow_html=True)
    cmp = pd.DataFrame({
        "Parameter":     ["V_DC (ideal)",  "V_RMS",    "Ripple Factor γ", "Efficiency η", "PIV",   "Diodes", "Centre-Tap?"],
        "Half-Wave":     ["0.318 Vₚ",      "Vₚ / 2",  "1.21",            "40.6%",        "Vₚ",    "1",      "No"],
        "FW Centre-Tap": ["0.636 Vₚ",      "Vₚ / √2", "0.482",           "81.2%",        "2Vₚ",   "2",      "Yes"],
        "FW Bridge":     ["0.636 Vₚ",      "Vₚ / √2", "0.482",           "81.2%",        "Vₚ",    "4",      "No"],
    })
    st.dataframe(cmp.set_index("Parameter"), use_container_width=True)

# ══════════════════════════════════════════════════════════
# TAB 3 — METRICS DASHBOARD
# ══════════════════════════════════════════════════════════
with tab3:
    st.markdown('<p class="section-header">// Parametric Sweep Analysis</p>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("**V_DC vs Peak Voltage (Vₚ)**")
        vp_range = np.linspace(1, 50, 200)
        if mode == "Half-Wave Rectifier":
            vdc_vals = np.maximum(vp_range - Vd, 0) / np.pi
        elif mode == "Full-Wave — Centre Tap":
            vdc_vals = 2 * np.maximum(vp_range - Vd, 0) / np.pi
        else:
            vdc_vals = 2 * np.maximum(vp_range - 2 * Vd, 0) / np.pi

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=vp_range, y=vdc_vals,
            line=dict(color=color_main, width=2.5),
            fill="tozeroy", fillcolor=fill_main,
            name="V_DC"
        ))
        fig2.add_trace(go.Scatter(
            x=[Vp, Vp],
            y=[0, float(vdc_vals[np.argmin(np.abs(vp_range - Vp))])],
            mode="lines",
            line=dict(color="#facc15", width=1.5, dash="dash"),
            name=f"Vₚ = {Vp} V"
        ))
        fig2.update_layout(
            template="plotly_dark", paper_bgcolor="#0b0f1a", plot_bgcolor="#0d1520",
            height=280, margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(title="Vₚ (V)", gridcolor="#1a2a3a"),
            yaxis=dict(title="V_DC (V)", gridcolor="#1a2a3a"),
            font=dict(family="Share Tech Mono", color="#c0d4e8", size=10),
            legend=dict(orientation="h", y=-0.3, bgcolor="rgba(0,0,0,0)")
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col_b:
        st.markdown("**Ripple Factor vs Capacitance (C)**")
        c_range      = np.linspace(1, 5000, 300)
        f_ripple     = freq * ripple_freq_mult
        vr_approx    = Vout_peak / (f_ripple * RL * c_range * 1e-6)
        vdc_approx   = np.clip(Vout_peak - vr_approx / 2, 0.001, Vout_peak)
        vac_approx   = vr_approx / (2 * np.sqrt(3))
        gamma_approx = vac_approx / vdc_approx

        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=c_range, y=gamma_approx,
            line=dict(color="#f0abfc", width=2.5),
            fill="tozeroy", fillcolor="rgba(240,171,252,0.08)",
            name="Ripple Factor γ"
        ))
        fig3.update_layout(
            template="plotly_dark", paper_bgcolor="#0b0f1a", plot_bgcolor="#0d1520",
            height=280, margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(title="Capacitance C (µF)", gridcolor="#1a2a3a"),
            yaxis=dict(title="Ripple Factor γ", gridcolor="#1a2a3a"),
            font=dict(family="Share Tech Mono", color="#c0d4e8", size=10),
            legend=dict(orientation="h", y=-0.3, bgcolor="rgba(0,0,0,0)")
        )
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<p class="section-header">// Detailed Computed Parameters</p>', unsafe_allow_html=True)
    params_df = pd.DataFrame({
        "Parameter": [
            "Peak Input Voltage (Vₚ)",    "RMS Input Voltage",
            "Peak Output Voltage",         "DC Output Voltage (V_DC)",
            "RMS Output Voltage",          "Peak Inverse Voltage (PIV)",
            "DC Load Current (I_DC)",      "Peak Load Current",
            "Ripple Voltage p-p",          "Ripple Factor (γ)",
            "Rectifier Efficiency (η)",    "Diodes Required",
        ],
        "Value": [
            f"{Vp:.1f} V",          f"{Vin_rms:.3f} V",
            f"{Vout_peak:.3f} V",   f"{Vout_dc:.3f} V",
            f"{Vout_rms:.3f} V",    f"{PIV:.2f} V",
            f"{Idc:.2f} mA",        f"{Ipeak:.2f} mA",
            f"{Vripple_pp:.4f} V",  f"{ripple_factor:.4f}",
            f"{eta:.2f} %",         str(n_diodes),
        ]
    })
    st.dataframe(params_df.set_index("Parameter"), use_container_width=True)

st.markdown("---")
st.caption(f"⚡ Rectification Lab · Student: `{st.session_state['student_id']}` · Session active")
