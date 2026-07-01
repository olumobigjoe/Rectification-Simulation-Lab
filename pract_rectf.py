import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import os

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Rectification Lab",
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
    [data-testid="stSidebar"] .stRadio label { color: #c0d4e8 !important; }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: #00d4ff; }

    .stSlider > div { padding: 0; }
    div[data-baseweb="slider"] { padding-top: 0; }
    .stSelectbox label, .stSlider label, .stRadio label { color: #c0d4e8 !important; font-size: 0.85rem !important; }

    .stTabs [data-baseweb="tab-list"] { background: #0d1520; border-bottom: 1px solid #1e3a5f; gap: 2px; }
    .stTabs [data-baseweb="tab"] { background: transparent; color: #7a9cc4; border: none; font-size: 0.85rem; font-family: 'Share Tech Mono', monospace; letter-spacing: 0.05em; }
    .stTabs [aria-selected="true"] { background: #111827 !important; color: #00d4ff !important; border-bottom: 2px solid #00d4ff !important; }

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
for key, default in [("auth", False), ("student_id", "")]:
    if key not in st.session_state:
        st.session_state[key] = default

# ─── HERO BANNER ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <p class="hero-title">⚡ Rectification Lab</p>
    <p class="hero-subtitle">Department of Electronics — Power Electronics Laboratory · Half-Wave &amp; Full-Wave Circuits</p>
</div>
""", unsafe_allow_html=True)

# ─── LOGIN GATE ──────────────────────────────────────────────────────────────
if not st.session_state["auth"]:
    st.markdown('<p class="section-header">// Laboratory Access</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.4, 1])
    with c2:
        st.markdown("Enter your **Matriculation Number** to initialise the lab bench.")
        matric = st.text_input("Matriculation Number", placeholder="e.g. ENG/2022/001")
        if st.button("▶  INITIALISE LAB BENCH"):
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
    Vp   = st.slider("Peak Voltage  Vₚ (V)", 1.0, 50.0, 12.0, 0.5)
    freq = st.slider("Frequency  f (Hz)", 10, 500, 50, 10)

    st.markdown("---")
    st.caption(f"👤 Student: `{st.session_state['student_id']}`")
    if st.button("🔒 Log Out"):
        st.session_state["auth"] = False
        st.rerun()

# ─── FIXED CIRCUIT CONSTANTS ─────────────────────────────────────────────────
Vd       = 0.7    # diode forward drop (V)
RL       = 500    # load resistance (Ω)
n_cycles = 3

# ─── SIGNAL GENERATION ───────────────────────────────────────────────────────
T     = 1.0 / freq
t     = np.linspace(0, n_cycles * T, 8000)
v_in  = Vp * np.sin(2 * np.pi * freq * t)

def half_wave(v, vd):
    return np.where(v > vd, v - vd, 0.0)

def full_wave_ct(v, vd):
    return np.where(np.abs(v) > vd, np.abs(v) - vd, 0.0)

def full_wave_bridge(v, vd):
    return np.where(np.abs(v) > 2 * vd, np.abs(v) - 2 * vd, 0.0)

# ─── TOPOLOGY SELECTION ──────────────────────────────────────────────────────
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

# ─── METRICS CALCULATION ─────────────────────────────────────────────────────
Vout_peak     = float(v_out.max())
Vout_dc       = float(v_out.mean())
Vout_rms      = float(np.sqrt(np.mean(v_out ** 2)))
Vin_rms       = float(np.sqrt(np.mean(v_in ** 2)))
Vripple_pp    = float(v_out.max() - v_out.min())
Vac_rms       = float(np.sqrt(max(Vout_rms ** 2 - Vout_dc ** 2, 0.0)))
ripple_factor = (Vac_rms / Vout_dc) if Vout_dc > 0 else 0.0
P_dc          = (Vout_dc ** 2) / RL
P_in          = (Vin_rms ** 2) / RL
eta           = (P_dc / P_in * 100) if P_in > 0 else 0.0
Idc           = Vout_dc   / RL * 1000   # mA
Ipeak         = Vout_peak / RL * 1000   # mA
PIV           = (2 * Vp - Vd) if mode == "Full-Wave — Centre Tap" else Vp

log_action(st.session_state["student_id"], "Signal_Generated",
           f"Mode={mode}, Vp={Vp}, f={freq}")

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

    # Metric cards
    def mcard(col, label, val, unit):
        col.markdown(f"""
        <div class="metric-card">
            <div class="label">{label}</div>
            <div class="value">{val}</div>
            <div class="unit">{unit}</div>
        </div>""", unsafe_allow_html=True)

    m1, m2, m3, m4, m5, m6 = st.columns(6)
    mcard(m1, "V_peak",       f"{Vout_peak:.2f}",   "V")
    mcard(m2, "V_DC",         f"{Vout_dc:.2f}",     "V")
    mcard(m3, "V_RMS",        f"{Vout_rms:.2f}",    "V")
    mcard(m4, "Ripple Factor",f"{ripple_factor:.4f}","γ")
    mcard(m5, "Efficiency",   f"{eta:.1f}",          "%")
    mcard(m6, "PIV",          f"{PIV:.2f}",          "V")

    st.markdown("")

    t_ms = t * 1000   # time axis in milliseconds

    fig = go.Figure()

    # AC input
    fig.add_trace(go.Scatter(
        x=t_ms, y=v_in,
        name="AC Input  vᵢₙ(t)",
        line=dict(color="#60a5fa", width=1.5, dash="dot"),
        opacity=0.65
    ))

    # Rectified output
    fig.add_trace(go.Scatter(
        x=t_ms, y=v_out,
        name=label_rect,
        line=dict(color=color_main, width=2.5),
        fill="tozeroy",
        fillcolor=fill_main
    ))

    # DC level as a horizontal scatter line (avoids add_hline version issues)
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
        xaxis=dict(title="Time (ms)",   gridcolor="#1a2a3a",
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
        • V_DC = Vₚ / π ≈ 0.318 Vₚ<br>
        • V_RMS = Vₚ / 2<br>
        • Ripple factor γ = 1.21 (without filter)<br>
        • Rectifier efficiency η = 40.6%<br>
        • PIV = Vₚ<br><br>
        Because only one half-cycle is used, this topology is the <em>least efficient</em> of the three.
        It is only suitable for very low power or signal applications.
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<p class="section-header">// Circuit Diagram</p>', unsafe_allow_html=True)
        st.markdown("""
        <svg viewBox="0 0 560 140" xmlns="http://www.w3.org/2000/svg"
             style="background:#0d1520;border-radius:8px;border:1px solid #1e3a5f;width:100%;max-width:560px;">
          <style>.w{stroke:#60a5fa;stroke-width:2;fill:none}
                 .t{fill:#c0d4e8;font-family:Share Tech Mono,monospace;font-size:12px}
                 .lbl{fill:#00d4ff;font-family:Share Tech Mono,monospace;font-size:11px}</style>
          <circle cx="60" cy="70" r="28" class="w"/>
          <text x="60" y="75" text-anchor="middle" class="t">~</text>
          <text x="60" y="118" text-anchor="middle" class="lbl">Vᵢₙ</text>
          <line x1="88" y1="42" x2="200" y2="42" class="w"/>
          <polygon points="200,30 200,54 228,42" style="fill:#4ade80;stroke:#4ade80;stroke-width:1"/>
          <line x1="228" y1="30" x2="228" y2="54" style="stroke:#4ade80;stroke-width:2.5"/>
          <text x="214" y="26" text-anchor="middle" class="lbl">D</text>
          <line x1="228" y1="42" x2="340" y2="42" class="w"/>
          <rect x="340" y="28" width="80" height="28" rx="4" style="fill:#1a2a1a;stroke:#4ade80;stroke-width:1.5"/>
          <text x="380" y="47" text-anchor="middle" class="lbl">Rₗ</text>
          <line x1="420" y1="42" x2="480" y2="42" class="w"/>
          <line x1="480" y1="42" x2="480" y2="98" class="w"/>
          <line x1="88"  y1="98" x2="480" y2="98" class="w"/>
          <text x="455" y="75" text-anchor="middle" class="lbl">Vₒᵤₜ</text>
          <line x1="450" y1="48" x2="450" y2="92" style="stroke:#facc15;stroke-width:1.5;stroke-dasharray:4,3"/>
          <line x1="447" y1="48" x2="453" y2="48" style="stroke:#facc15;stroke-width:1.5"/>
          <line x1="447" y1="92" x2="453" y2="92" style="stroke:#facc15;stroke-width:1.5"/>
        </svg>
        """, unsafe_allow_html=True)

    elif mode == "Full-Wave — Centre Tap":
        st.markdown("""
        <div class="theory-box">
        <strong>Full-Wave Centre-Tap Rectifier</strong><br><br>
        This uses a <strong>centre-tapped transformer</strong> and two diodes. The centre tap serves as the
        ground reference. During the positive half-cycle, diode D₁ conducts; during the negative half-cycle,
        diode D₂ conducts. <em>Both half-cycles appear at the output</em>, doubling the ripple frequency.<br><br>
        <strong>Key equations:</strong><br>
        • V_DC = 2Vₚ / π ≈ 0.636 Vₚ<br>
        • V_RMS = Vₚ / √2<br>
        • Ripple factor γ = 0.482 (without filter)<br>
        • Rectifier efficiency η = 81.2%<br>
        • PIV = 2Vₚ − Vd (each diode must block the full secondary voltage)<br><br>
        The high PIV requirement means diodes with a higher voltage rating are needed compared to
        the bridge circuit, which is a practical disadvantage.
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<p class="section-header">// Circuit Diagram</p>', unsafe_allow_html=True)
        st.markdown("""
        <svg viewBox="0 0 580 160" xmlns="http://www.w3.org/2000/svg"
             style="background:#0d1520;border-radius:8px;border:1px solid #1e3a5f;width:100%;max-width:580px;">
          <style>.w{stroke:#60a5fa;stroke-width:2;fill:none}
                 .t{fill:#c0d4e8;font-family:Share Tech Mono,monospace;font-size:12px}
                 .lbl{fill:#818cf8;font-family:Share Tech Mono,monospace;font-size:11px}</style>
          <rect x="20" y="30" width="60" height="100" rx="4" style="fill:#0d1520;stroke:#60a5fa;stroke-width:1.5"/>
          <text x="50" y="85" text-anchor="middle" class="t">~</text>
          <text x="50" y="145" text-anchor="middle" class="lbl">Transformer</text>
          <line x1="80" y1="40"  x2="160" y2="40"  class="w"/>
          <line x1="80" y1="120" x2="160" y2="120" class="w"/>
          <line x1="80" y1="80"  x2="360" y2="80"
                style="stroke:#60a5fa;stroke-width:1.5;stroke-dasharray:4,3"/>
          <polygon points="160,28 160,52 188,40" style="fill:#818cf8;stroke:#818cf8;stroke-width:1"/>
          <line x1="188" y1="28" x2="188" y2="52" style="stroke:#818cf8;stroke-width:2.5"/>
          <text x="174" y="22" text-anchor="middle" class="lbl">D₁</text>
          <polygon points="160,108 160,132 188,120" style="fill:#818cf8;stroke:#818cf8;stroke-width:1"/>
          <line x1="188" y1="108" x2="188" y2="132" style="stroke:#818cf8;stroke-width:2.5"/>
          <text x="174" y="145" text-anchor="middle" class="lbl">D₂</text>
          <line x1="188" y1="40"  x2="300" y2="40"  class="w"/>
          <line x1="188" y1="120" x2="300" y2="120" class="w"/>
          <line x1="300" y1="40"  x2="300" y2="60"  class="w"/>
          <line x1="300" y1="120" x2="300" y2="100" class="w"/>
          <rect x="340" y="55" width="70" height="50" rx="4"
                style="fill:#1a1a2a;stroke:#818cf8;stroke-width:1.5"/>
          <text x="375" y="85" text-anchor="middle" class="lbl">Rₗ</text>
          <line x1="300" y1="80" x2="340" y2="80" class="w"/>
          <line x1="410" y1="80" x2="480" y2="80" class="w"/>
          <text x="338" y="74" text-anchor="end" class="lbl">CT</text>
        </svg>
        """, unsafe_allow_html=True)

    else:  # Bridge
        st.markdown("""
        <div class="theory-box">
        <strong>Full-Wave Bridge Rectifier</strong><br><br>
        Four diodes are arranged in a <strong>bridge configuration</strong>. No centre-tap transformer is needed.
        During the positive half-cycle, D₁ and D₃ conduct; during the negative half-cycle, D₂ and D₄ conduct.
        Current through the load always flows in the <em>same direction</em>.<br><br>
        <strong>Key equations:</strong><br>
        • V_DC = 2Vₚ / π ≈ 0.636 Vₚ  (but 2×Vd loss)<br>
        • V_RMS = Vₚ / √2<br>
        • Ripple factor γ = 0.482 (without filter)<br>
        • Rectifier efficiency η = 81.2%<br>
        • PIV = Vₚ − Vd (much lower than centre-tap, so cheaper diodes can be used)<br><br>
        The bridge is the <em>most widely used</em> rectifier topology in power supplies because it does not
        require a centre-tap and has a lower PIV requirement per diode.
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<p class="section-header">// Circuit Diagram</p>', unsafe_allow_html=True)
        st.markdown("""
        <svg viewBox="0 0 560 200" xmlns="http://www.w3.org/2000/svg"
             style="background:#0d1520;border-radius:8px;border:1px solid #1e3a5f;width:100%;max-width:560px;">
          <style>.w{stroke:#60a5fa;stroke-width:2;fill:none}
                 .lbl{fill:#fb923c;font-family:Share Tech Mono,monospace;font-size:11px}</style>
          <circle cx="60" cy="100" r="28" class="w"/>
          <text x="60" y="105" text-anchor="middle"
                style="fill:#c0d4e8;font-family:monospace;font-size:14px">~</text>
          <line x1="88" y1="72"  x2="200" y2="72"  class="w"/>
          <line x1="88" y1="128" x2="200" y2="128" class="w"/>
          <polygon points="200,100 220,68 240,84"   style="fill:#fb923c;stroke:#fb923c"/>
          <line x1="240" y1="60" x2="240" y2="92"  style="stroke:#fb923c;stroke-width:2.5"/>
          <text x="210" y="60" class="lbl">D₁</text>
          <polygon points="280,52 300,68 280,84"    style="fill:#fb923c;stroke:#fb923c"/>
          <line x1="278" y1="52" x2="278" y2="84"  style="stroke:#fb923c;stroke-width:2.5"/>
          <text x="292" y="60" class="lbl">D₃</text>
          <polygon points="200,100 220,130 240,114" style="fill:#fb923c;stroke:#fb923c"/>
          <line x1="240" y1="108" x2="240" y2="140" style="stroke:#fb923c;stroke-width:2.5"/>
          <text x="210" y="155" class="lbl">D₄</text>
          <polygon points="280,116 300,132 280,148" style="fill:#fb923c;stroke:#fb923c"/>
          <line x1="278" y1="116" x2="278" y2="148" style="stroke:#fb923c;stroke-width:2.5"/>
          <text x="292" y="155" class="lbl">D₂</text>
          <line x1="200" y1="72"  x2="200" y2="100" class="w"/>
          <line x1="200" y1="100" x2="200" y2="128" class="w"/>
          <line x1="240" y1="72"  x2="280" y2="72"  class="w"/>
          <line x1="240" y1="128" x2="280" y2="128" class="w"/>
          <line x1="280" y1="72"  x2="280" y2="52"  class="w"/>
          <line x1="280" y1="128" x2="280" y2="148" class="w"/>
          <line x1="280" y1="52"  x2="360" y2="52"  class="w"/>
          <line x1="280" y1="148" x2="360" y2="148" class="w"/>
          <rect x="360" y="80" width="70" height="40" rx="4"
                style="fill:#2a1a0a;stroke:#fb923c;stroke-width:1.5"/>
          <text x="395" y="105" text-anchor="middle" class="lbl">Rₗ</text>
          <line x1="360" y1="52"  x2="430" y2="52"  class="w"/>
          <line x1="430" y1="52"  x2="430" y2="80"  class="w"/>
          <line x1="360" y1="148" x2="430" y2="148" class="w"/>
          <line x1="430" y1="148" x2="430" y2="120" class="w"/>
        </svg>
        """, unsafe_allow_html=True)

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
            fill="tozeroy",
            fillcolor=fill_main,
            name="V_DC"
        ))
        # current Vp marker
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
            legend=dict(orientation="h", y=-0.25, bgcolor="rgba(0,0,0,0)")
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col_b:
        st.markdown("**Ripple Factor vs Capacitance (C)**")
        c_range    = np.linspace(1, 5000, 300)
        f_ripple   = freq * ripple_freq_mult
        vr_approx  = Vout_peak / (f_ripple * RL * c_range * 1e-6)
        vdc_approx = np.clip(Vout_peak - vr_approx / 2, 0.001, Vout_peak)
        vac_approx = vr_approx / (2 * np.sqrt(3))
        gamma_approx = vac_approx / vdc_approx

        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=c_range, y=gamma_approx,
            line=dict(color="#f0abfc", width=2.5),
            fill="tozeroy",
            fillcolor="rgba(240,171,252,0.08)",
            name="Ripple Factor γ"
        ))
        fig3.update_layout(
            template="plotly_dark", paper_bgcolor="#0b0f1a", plot_bgcolor="#0d1520",
            height=280, margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(title="Capacitance C (µF)", gridcolor="#1a2a3a"),
            yaxis=dict(title="Ripple Factor γ", gridcolor="#1a2a3a"),
            font=dict(family="Share Tech Mono", color="#c0d4e8", size=10),
            legend=dict(orientation="h", y=-0.25, bgcolor="rgba(0,0,0,0)")
        )
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<p class="section-header">// Detailed Computed Parameters</p>', unsafe_allow_html=True)
    params_df = pd.DataFrame({
        "Parameter": [
            "Peak Input Voltage (Vₚ)",     "RMS Input Voltage",
            "Peak Output Voltage",          "DC Output Voltage (V_DC)",
            "RMS Output Voltage",           "Peak Inverse Voltage (PIV)",
            "DC Load Current (I_DC)",       "Peak Load Current",
            "Ripple Voltage p-p",           "Ripple Factor (γ)",
            "Rectifier Efficiency (η)",     "Diodes Required",
        ],
        "Value": [
            f"{Vp:.2f} V",          f"{Vin_rms:.3f} V",
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
