import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import os

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Rectification Lab",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Inter:wght@300;400;600;700&display=swap');

    /* Base */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .stApp {
        background: #0b0f1a;
        color: #e0e6f0;
    }

    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #0d1b2a 0%, #11213a 50%, #0a1628 100%);
        border: 1px solid #1e3a5f;
        border-radius: 12px;
        padding: 28px 36px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    .hero-banner::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00d4ff, #0080ff, transparent);
    }
    .hero-title {
        font-family: 'Share Tech Mono', monospace;
        font-size: 2rem;
        color: #00d4ff;
        margin: 0;
        letter-spacing: 0.05em;
    }
    .hero-subtitle {
        font-size: 0.9rem;
        color: #7a9cc4;
        margin-top: 6px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    /* Metric Cards */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 12px;
        margin: 16px 0;
    }
    .metric-card {
        background: #111827;
        border: 1px solid #1e3a5f;
        border-radius: 8px;
        padding: 14px 16px;
        text-align: center;
    }
    .metric-card .label {
        font-size: 0.7rem;
        color: #7a9cc4;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    .metric-card .value {
        font-family: 'Share Tech Mono', monospace;
        font-size: 1.5rem;
        color: #00d4ff;
        margin-top: 4px;
    }
    .metric-card .unit {
        font-size: 0.7rem;
        color: #4a7a9b;
    }

    /* Theory Box */
    .theory-box {
        background: #0d1b2a;
        border-left: 3px solid #0080ff;
        border-radius: 0 8px 8px 0;
        padding: 16px 20px;
        margin: 12px 0;
        font-size: 0.88rem;
        color: #c0d4e8;
        line-height: 1.65;
    }
    .theory-box strong { color: #00d4ff; }

    /* Mode Selector */
    .mode-chip {
        display: inline-block;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    .chip-half { background: #1a2a1a; color: #4ade80; border: 1px solid #4ade80; }
    .chip-full-ct { background: #1a1a2a; color: #818cf8; border: 1px solid #818cf8; }
    .chip-full-br { background: #2a1a1a; color: #fb923c; border: 1px solid #fb923c; }

    /* Section Headers */
    .section-header {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.8rem;
        color: #00d4ff;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        border-bottom: 1px solid #1e3a5f;
        padding-bottom: 6px;
        margin: 20px 0 12px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #0d1520;
        border-right: 1px solid #1e3a5f;
    }
    [data-testid="stSidebar"] .stRadio label {
        color: #c0d4e8 !important;
    }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #00d4ff;
    }

    /* Quiz */
    .quiz-result-pass {
        background: #0a2a15;
        border: 1px solid #4ade80;
        border-radius: 8px;
        padding: 16px;
        color: #4ade80;
    }
    .quiz-result-fail {
        background: #2a1515;
        border: 1px solid #f87171;
        border-radius: 8px;
        padding: 16px;
        color: #f87171;
    }

    /* Override streamlit defaults */
    .stSlider > div { padding: 0; }
    div[data-baseweb="slider"] { padding-top: 0; }
    .stSelectbox label, .stSlider label, .stRadio label {
        color: #c0d4e8 !important;
        font-size: 0.85rem !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        background: #0d1520;
        border-bottom: 1px solid #1e3a5f;
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #7a9cc4;
        border: none;
        font-size: 0.85rem;
        font-family: 'Share Tech Mono', monospace;
        letter-spacing: 0.05em;
    }
    .stTabs [aria-selected="true"] {
        background: #111827 !important;
        color: #00d4ff !important;
        border-bottom: 2px solid #00d4ff !important;
    }
    .stButton > button {
        background: #0d2a4a;
        color: #00d4ff;
        border: 1px solid #0080ff;
        border-radius: 6px;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.8rem;
        letter-spacing: 0.05em;
        transition: all 0.2s;
        width: 100%;
    }
    .stButton > button:hover {
        background: #0f3d6e;
        border-color: #00d4ff;
    }
</style>
""", unsafe_allow_html=True)

# ─── ANALYTICS LOGGER ────────────────────────────────────────────────────────
LOG_FILE = "rectification_lab_log.csv"

def log_action(student_id, action, details=""):
    entry = pd.DataFrame([{
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Student_ID": student_id,
        "Action": action,
        "Details": str(details)
    }])
    if not os.path.isfile(LOG_FILE):
        entry.to_csv(LOG_FILE, index=False)
    else:
        entry.to_csv(LOG_FILE, mode='a', header=False, index=False)

# ─── SESSION STATE ────────────────────────────────────────────────────────────
for key, default in [
    ("auth", False), ("student_id", ""), ("quiz_submitted", False), ("quiz_score", 0)
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ─── HERO BANNER ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <p class="hero-title">⚡ Rectification Lab</p>
    <p class="hero-subtitle">Department of Electronics — Power Electronics Laboratory · Half-Wave & Full-Wave Circuits</p>
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

# ─── SIDEBAR CONTROLS ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Circuit Parameters")

    mode = st.selectbox(
        "Rectifier Type",
        ["Half-Wave Rectifier", "Full-Wave — Centre Tap", "Full-Wave — Bridge"],
        help="Select the rectifier topology to simulate."
    )

    st.markdown("---")
    st.markdown("### AC Source")
    Vp = st.slider("Peak Voltage  Vₚ (V)", 1.0, 50.0, 12.0, 0.5)
    freq = st.slider("Frequency  f (Hz)", 10, 500, 50, 10)

    st.markdown("### Circuit Components")
    if mode == "Half-Wave Rectifier":
        Vd = st.slider("Diode Forward Drop  Vd (V)", 0.0, 1.0, 0.7, 0.05)
    elif mode == "Full-Wave — Centre Tap":
        Vd = st.slider("Diode Forward Drop  Vd (V)", 0.0, 1.0, 0.7, 0.05)
    else:  # Bridge
        Vd = st.slider("Diode Forward Drop  Vd (V)", 0.0, 1.0, 0.7, 0.05)

    RL = st.slider("Load Resistance  Rₗ (Ω)", 10, 2000, 500, 10)
    use_cap = st.toggle("Add Filter Capacitor", value=False)
    if use_cap:
        C = st.slider("Capacitance  C (µF)", 1, 10000, 100, 10)
    else:
        C = 0

    st.markdown("---")
    st.markdown("### Display")
    n_cycles = st.slider("AC Cycles to Display", 1, 6, 3)
    show_input = st.checkbox("Overlay AC Input", value=True)
    show_ripple = st.checkbox("Show Ripple Annotation", value=True)

    st.markdown("---")
    st.caption(f"👤 Student: `{st.session_state['student_id']}`")
    if st.button("🔒 Log Out"):
        st.session_state["auth"] = False
        st.rerun()

# ─── SIGNAL GENERATION ───────────────────────────────────────────────────────
T = 1.0 / freq
t_end = n_cycles * T
t = np.linspace(0, t_end, 8000)
v_in = Vp * np.sin(2 * np.pi * freq * t)

def half_wave(v_in, Vd):
    out = np.where(v_in > Vd, v_in - Vd, 0.0)
    return out

def full_wave_ct(v_in, Vd):
    # Centre-tap: both halves rectified, each diode drops Vd
    out = np.abs(v_in) - Vd
    out = np.where(out < 0, 0.0, out)
    return out

def full_wave_bridge(v_in, Vd):
    # Bridge: 2 diodes in series each half cycle
    out = np.abs(v_in) - 2 * Vd
    out = np.where(out < 0, 0.0, out)
    return out

def apply_capacitor_filter(t, v_rect, C, RL, freq_ripple):
    """Simulate RC filter by exponential decay between peaks."""
    if C == 0 or RL == 0:
        return v_rect.copy()
    tau = RL * C * 1e-6
    out = v_rect.copy()
    dt = t[1] - t[0]
    for i in range(1, len(out)):
        # If rectified signal is above the capacitor voltage → charge
        if v_rect[i] >= out[i - 1]:
            out[i] = v_rect[i]
        else:
            # Discharge through load
            out[i] = out[i - 1] * np.exp(-dt / tau)
    return out

# Compute rectified waveforms
if mode == "Half-Wave Rectifier":
    v_rect_raw = half_wave(v_in, Vd)
    color_main = "#4ade80"
    label_rect = "Half-Wave Output"
    n_diodes = 1
    ripple_freq_mult = 1  # ripple at f
elif mode == "Full-Wave — Centre Tap":
    v_rect_raw = full_wave_ct(v_in, Vd)
    color_main = "#818cf8"
    label_rect = "Full-Wave CT Output"
    n_diodes = 2
    ripple_freq_mult = 2
else:
    v_rect_raw = full_wave_bridge(v_in, Vd)
    color_main = "#fb923c"
    label_rect = "Bridge Rectifier Output"
    n_diodes = 4
    ripple_freq_mult = 2

v_filtered = apply_capacitor_filter(t, v_rect_raw, C, RL, freq * ripple_freq_mult)
v_out = v_filtered

# ─── METRICS ─────────────────────────────────────────────────────────────────
Vout_peak = v_out.max()
Vout_dc   = v_out.mean()
Vout_rms  = np.sqrt(np.mean(v_out**2))
Vin_rms   = np.sqrt(np.mean(v_in**2))

# Ripple voltage = Vpp of output after DC component
Vripple_pp = v_out.max() - v_out.min()
# Ripple factor γ = V_ac_rms / V_dc
Vac_rms = np.sqrt(max(Vout_rms**2 - Vout_dc**2, 0))
ripple_factor = (Vac_rms / Vout_dc) if Vout_dc > 0 else 0

# Rectifier efficiency η = P_dc / P_ac_in
P_dc  = (Vout_dc**2) / RL
P_in  = (Vin_rms**2) / RL
eta   = (P_dc / P_in * 100) if P_in > 0 else 0

Idc   = Vout_dc / RL * 1000   # mA
Ipeak = Vout_peak / RL * 1000  # mA

# PIV (Peak Inverse Voltage)
if mode == "Half-Wave Rectifier":
    PIV = Vp
elif mode == "Full-Wave — Centre Tap":
    PIV = 2 * Vp - Vd
else:
    PIV = Vp

log_action(st.session_state["student_id"], "Signal_Generated",
           f"Mode={mode}, Vp={Vp}, f={freq}, RL={RL}, C={C}")

# ─── MAIN TABS ────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📈  WAVEFORM ANALYSER",
    "📐  CIRCUIT THEORY",
    "📊  METRICS DASHBOARD",
    "📝  VIVA-VOCE QUIZ"
])

# ══════════════════════════════════════════════════════════
# TAB 1 — WAVEFORM
# ══════════════════════════════════════════════════════════
with tab1:
    # Metrics row at top
    st.markdown('<p class="section-header">// Live Waveform Measurements</p>', unsafe_allow_html=True)

    m1, m2, m3, m4, m5, m6 = st.columns(6)
    def mcard(col, label, val, unit):
        col.markdown(f"""
        <div class="metric-card">
            <div class="label">{label}</div>
            <div class="value">{val}</div>
            <div class="unit">{unit}</div>
        </div>""", unsafe_allow_html=True)

    mcard(m1, "V_peak", f"{Vout_peak:.2f}", "V")
    mcard(m2, "V_DC", f"{Vout_dc:.2f}", "V")
    mcard(m3, "V_RMS", f"{Vout_rms:.2f}", "V")
    mcard(m4, "Ripple Factor", f"{ripple_factor:.4f}", "γ")
    mcard(m5, "Efficiency", f"{eta:.1f}", "%")
    mcard(m6, "PIV", f"{PIV:.2f}", "V")

    st.markdown("")

    # Build plot
    rows = 2 if use_cap else 1
    subplot_titles = (
        ["AC Input vs Rectified Output", "Filter Capacitor Effect"]
        if use_cap else ["AC Input vs Rectified Output"]
    )
    fig = make_subplots(
        rows=rows, cols=1,
        shared_xaxes=True,
        subplot_titles=subplot_titles,
        vertical_spacing=0.08,
        row_heights=[1.0] if not use_cap else [0.5, 0.5]
    )

    # Input AC
    if show_input:
        fig.add_trace(go.Scatter(
            x=t * 1000, y=v_in,
            name="AC Input  vᵢₙ(t)",
            line=dict(color="#60a5fa", width=1.5, dash="dot"),
            opacity=0.65
        ), row=1, col=1)

    # Rectified (unfiltered) line in lighter shade
    if use_cap:
        fig.add_trace(go.Scatter(
            x=t * 1000, y=v_rect_raw,
            name="Rectified (unfiltered)",
            line=dict(color=color_main, width=1, dash="dot"),
            opacity=0.4
        ), row=1, col=1)

    # Main output
    fig.add_trace(go.Scatter(
        x=t * 1000, y=v_out,
        name=label_rect + (" + Filter" if use_cap else ""),
        line=dict(color=color_main, width=2.5),
        fill="tozeroy",
        fillcolor=color_main.replace(")", ", 0.06)").replace("rgb", "rgba") if "rgb" in color_main else color_main + "12"
    ), row=1, col=1)

    # DC level line
    fig.add_hline(
        y=Vout_dc, line=dict(color="#facc15", dash="dash", width=1.5),
        annotation_text=f"  V_DC = {Vout_dc:.2f} V",
        annotation_font=dict(color="#facc15", size=11),
        row=1, col=1
    )

    # Ripple annotation
    if show_ripple and Vripple_pp > 0.01 and use_cap:
        max_idx = np.argmax(v_out)
        min_idx = np.argmin(v_out[max_idx:]) + max_idx
        fig.add_annotation(
            x=t[min_idx] * 1000, y=(v_out.max() + v_out[min_idx]) / 2,
            ax=t[min_idx] * 1000, ay=v_out.max(),
            xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=2, arrowcolor="#f87171",
            text=f"Vᵣ = {Vripple_pp:.3f} V",
            font=dict(color="#f87171", size=10),
            row=1, col=1
        )

    if use_cap:
        # Bottom subplot: compare raw vs filtered
        fig.add_trace(go.Scatter(
            x=t * 1000, y=v_rect_raw,
            name="Before Filter",
            line=dict(color=color_main, width=1.5, dash="dot"),
            opacity=0.6
        ), row=2, col=1)
        fig.add_trace(go.Scatter(
            x=t * 1000, y=v_filtered,
            name="After Filter",
            line=dict(color="#f0abfc", width=2)
        ), row=2, col=1)

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0b0f1a",
        plot_bgcolor="#0d1520",
        font=dict(family="Share Tech Mono, monospace", color="#c0d4e8", size=11),
        legend=dict(
            orientation="h", y=-0.18, x=0,
            bgcolor="rgba(0,0,0,0)",
            bordercolor="#1e3a5f"
        ),
        margin=dict(l=10, r=10, t=30, b=10),
        height=480 if not use_cap else 620,
        xaxis=dict(
            title="Time (ms)",
            gridcolor="#1a2a3a", zeroline=True, zerolinecolor="#1e3a5f"
        ),
        yaxis=dict(
            title="Voltage (V)",
            gridcolor="#1a2a3a", zeroline=True, zerolinecolor="#1e3a5f"
        ),
    )
    if use_cap:
        fig.update_xaxes(title_text="Time (ms)", gridcolor="#1a2a3a", row=2, col=1)
        fig.update_yaxes(title_text="Voltage (V)", gridcolor="#1a2a3a", row=2, col=1)

    st.plotly_chart(fig, use_container_width=True)

    # Download data
    with st.expander("⬇️  Export Waveform Data"):
        export_df = pd.DataFrame({
            "Time (ms)": np.round(t * 1000, 4),
            "AC Input (V)": np.round(v_in, 4),
            "Rectified Output (V)": np.round(v_out, 4),
        })
        st.download_button(
            "Download as CSV",
            data=export_df.to_csv(index=False),
            file_name=f"rectification_{mode.replace(' ','_').lower()}.csv",
            mime="text/csv"
        )

# ══════════════════════════════════════════════════════════
# TAB 2 — THEORY
# ══════════════════════════════════════════════════════════
with tab2:
    st.markdown('<p class="section-header">// Circuit Theory & Operation</p>', unsafe_allow_html=True)

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

        # Schematic SVG
        st.markdown('<p class="section-header">// Circuit Diagram</p>', unsafe_allow_html=True)
        st.markdown("""
        <svg viewBox="0 0 560 140" xmlns="http://www.w3.org/2000/svg" style="background:#0d1520;border-radius:8px;border:1px solid #1e3a5f;width:100%;max-width:560px;">
          <style>.w{stroke:#60a5fa;stroke-width:2;fill:none}.t{fill:#c0d4e8;font-family:Share Tech Mono,monospace;font-size:12px}.lbl{fill:#00d4ff;font-family:Share Tech Mono,monospace;font-size:11px}</style>
          <!-- Input AC Source -->
          <circle cx="60" cy="70" r="28" class="w"/>
          <text x="60" y="75" text-anchor="middle" class="t">~</text>
          <text x="60" y="118" text-anchor="middle" class="lbl">Vᵢₙ</text>
          <!-- Top wire to diode -->
          <line x1="88" y1="42" x2="200" y2="42" class="w"/>
          <!-- Diode symbol -->
          <polygon points="200,30 200,54 228,42" style="fill:#4ade80;stroke:#4ade80;stroke-width:1"/>
          <line x1="228" y1="30" x2="228" y2="54" style="stroke:#4ade80;stroke-width:2.5"/>
          <text x="214" y="26" text-anchor="middle" class="lbl">D</text>
          <!-- Wire after diode -->
          <line x1="228" y1="42" x2="340" y2="42" class="w"/>
          <!-- Load Resistor -->
          <rect x="340" y="28" width="80" height="28" rx="4" style="fill:#1a2a1a;stroke:#4ade80;stroke-width:1.5"/>
          <text x="380" y="47" text-anchor="middle" class="lbl">Rₗ</text>
          <!-- Right side wire down -->
          <line x1="420" y1="42" x2="480" y2="42" class="w"/>
          <line x1="480" y1="42" x2="480" y2="98" class="w"/>
          <!-- Bottom return wire -->
          <line x1="88" y1="98" x2="480" y2="98" class="w"/>
          <!-- Vout label -->
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
        <svg viewBox="0 0 580 160" xmlns="http://www.w3.org/2000/svg" style="background:#0d1520;border-radius:8px;border:1px solid #1e3a5f;width:100%;max-width:580px;">
          <style>.w{stroke:#60a5fa;stroke-width:2;fill:none}.t{fill:#c0d4e8;font-family:Share Tech Mono,monospace;font-size:12px}.lbl{fill:#818cf8;font-family:Share Tech Mono,monospace;font-size:11px}</style>
          <!-- Transformer primary -->
          <rect x="20" y="30" width="60" height="100" rx="4" style="fill:#0d1520;stroke:#60a5fa;stroke-width:1.5"/>
          <text x="50" y="85" text-anchor="middle" class="t">~</text>
          <text x="50" y="145" text-anchor="middle" class="lbl">Transformer</text>
          <!-- Secondary taps -->
          <line x1="80" y1="40" x2="160" y2="40" class="w"/>
          <line x1="80" y1="120" x2="160" y2="120" class="w"/>
          <line x1="80" y1="80" x2="360" y2="80" style="stroke:#60a5fa;stroke-width:1.5;stroke-dasharray:4,3"/>
          <!-- D1 top -->
          <polygon points="160,28 160,52 188,40" style="fill:#818cf8;stroke:#818cf8;stroke-width:1"/>
          <line x1="188" y1="28" x2="188" y2="52" style="stroke:#818cf8;stroke-width:2.5"/>
          <text x="174" y="22" text-anchor="middle" class="lbl">D₁</text>
          <!-- D2 bottom -->
          <polygon points="160,108 160,132 188,120" style="fill:#818cf8;stroke:#818cf8;stroke-width:1"/>
          <line x1="188" y1="108" x2="188" y2="132" style="stroke:#818cf8;stroke-width:2.5"/>
          <text x="174" y="145" text-anchor="middle" class="lbl">D₂</text>
          <!-- Wires from diodes to load -->
          <line x1="188" y1="40" x2="300" y2="40" class="w"/>
          <line x1="188" y1="120" x2="300" y2="120" class="w"/>
          <line x1="300" y1="40" x2="300" y2="60" class="w"/>
          <line x1="300" y1="120" x2="300" y2="100" class="w"/>
          <!-- Load -->
          <rect x="340" y="55" width="70" height="50" rx="4" style="fill:#1a1a2a;stroke:#818cf8;stroke-width:1.5"/>
          <text x="375" y="85" text-anchor="middle" class="lbl">Rₗ</text>
          <line x1="300" y1="80" x2="340" y2="80" class="w"/>
          <line x1="410" y1="80" x2="480" y2="80" class="w"/>
          <!-- Centre tap ground -->
          <text x="340" y="74" text-anchor="end" class="lbl">CT</text>
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
        <svg viewBox="0 0 560 200" xmlns="http://www.w3.org/2000/svg" style="background:#0d1520;border-radius:8px;border:1px solid #1e3a5f;width:100%;max-width:560px;">
          <style>.w{stroke:#60a5fa;stroke-width:2;fill:none}.lbl{fill:#fb923c;font-family:Share Tech Mono,monospace;font-size:11px}</style>
          <!-- AC Source -->
          <circle cx="60" cy="100" r="28" class="w"/>
          <text x="60" y="105" text-anchor="middle" style="fill:#c0d4e8;font-family:monospace;font-size:14px">~</text>
          <!-- Wires from source -->
          <line x1="88" y1="72" x2="200" y2="72" class="w"/>
          <line x1="88" y1="128" x2="200" y2="128" class="w"/>
          <!-- Bridge diamond: 4 nodes at top(T), bottom(B), left(L), right(R) -->
          <!-- L=200,100  T=280,40  R=360,100  B=280,160 -->
          <!-- D1: L→T -->
          <polygon points="200,100 220,68 240,84" style="fill:#fb923c;stroke:#fb923c"/>
          <line x1="240" y1="60" x2="240" y2="92" style="stroke:#fb923c;stroke-width:2.5"/>
          <text x="210" y="60" class="lbl">D₁</text>
          <!-- D3: T→R -->
          <polygon points="280,52 300,68 280,84" style="fill:#fb923c;stroke:#fb923c"/>
          <line x1="278" y1="52" x2="278" y2="84" style="stroke:#fb923c;stroke-width:2.5"/>
          <text x="292" y="60" class="lbl">D₃</text>
          <!-- D4: L→B -->
          <polygon points="200,100 220,130 240,114" style="fill:#fb923c;stroke:#fb923c"/>
          <line x1="240" y1="108" x2="240" y2="140" style="stroke:#fb923c;stroke-width:2.5"/>
          <text x="210" y="155" class="lbl">D₄</text>
          <!-- D2: B→R -->
          <polygon points="280,116 300,132 280,148" style="fill:#fb923c;stroke:#fb923c"/>
          <line x1="278" y1="116" x2="278" y2="148" style="stroke:#fb923c;stroke-width:2.5"/>
          <text x="292" y="155" class="lbl">D₂</text>
          <!-- Wires to bridge corners -->
          <line x1="200" y1="72" x2="200" y2="100" class="w"/>
          <line x1="200" y1="100" x2="200" y2="128" class="w"/>
          <line x1="240" y1="72" x2="280" y2="72" class="w"/>
          <line x1="240" y1="128" x2="280" y2="128" class="w"/>
          <line x1="280" y1="72" x2="280" y2="52" class="w"/>
          <line x1="280" y1="128" x2="280" y2="148" class="w"/>
          <!-- Right side node to load -->
          <line x1="280" y1="52" x2="360" y2="52" class="w"/>
          <line x1="280" y1="148" x2="360" y2="148" class="w"/>
          <!-- Load Resistor -->
          <rect x="360" y="80" width="70" height="40" rx="4" style="fill:#2a1a0a;stroke:#fb923c;stroke-width:1.5"/>
          <text x="395" y="105" text-anchor="middle" class="lbl">Rₗ</text>
          <line x1="360" y1="52" x2="430" y2="52" class="w"/>
          <line x1="430" y1="52" x2="430" y2="80" class="w"/>
          <line x1="360" y1="148" x2="430" y2="148" class="w"/>
          <line x1="430" y1="148" x2="430" y2="120" class="w"/>
        </svg>
        """, unsafe_allow_html=True)

    # Comparison table
    st.markdown('<p class="section-header">// Comparative Summary</p>', unsafe_allow_html=True)
    cmp = pd.DataFrame({
        "Parameter":     ["V_DC (ideal)",    "V_RMS",     "Ripple Factor γ", "Efficiency η", "PIV",        "Diodes Required", "Transformer CT?"],
        "Half-Wave":     ["0.318 Vₚ",        "Vₚ / 2",   "1.21",            "40.6%",        "Vₚ",         "1",               "No"],
        "FW Centre-Tap": ["0.636 Vₚ",        "Vₚ / √2",  "0.482",           "81.2%",        "2Vₚ",        "2",               "Yes"],
        "FW Bridge":     ["0.636 Vₚ",        "Vₚ / √2",  "0.482",           "81.2%",        "Vₚ",         "4",               "No"],
    })
    st.dataframe(cmp.set_index("Parameter"), use_container_width=True)

# ══════════════════════════════════════════════════════════
# TAB 3 — METRICS DASHBOARD
# ══════════════════════════════════════════════════════════
with tab3:
    st.markdown('<p class="section-header">// Parametric Sweep Analysis</p>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        # Sweep Vp, plot Vdc vs Vp
        st.markdown("**V_DC vs Peak Voltage (Vₚ)**")
        vp_range = np.linspace(1, 50, 100)
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
            name="V_DC"
        ))
        fig2.add_vline(x=Vp, line=dict(color="#facc15", dash="dash", width=1.5),
                       annotation_text=f"  Vₚ = {Vp}V", annotation_font_color="#facc15")
        fig2.update_layout(
            template="plotly_dark", paper_bgcolor="#0b0f1a", plot_bgcolor="#0d1520",
            height=260, margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(title="Vₚ (V)", gridcolor="#1a2a3a"),
            yaxis=dict(title="V_DC (V)", gridcolor="#1a2a3a"),
            font=dict(family="Share Tech Mono", color="#c0d4e8", size=10)
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col_b:
        # Ripple factor vs capacitance
        st.markdown("**Ripple Factor vs Capacitance (C)**")
        c_range = np.linspace(1, 5000, 200)
        # Approximate ripple voltage: Vr ≈ Vp / (f_ripple * RL * C)
        f_ripple = freq * ripple_freq_mult
        vr_approx = Vout_peak / (f_ripple * RL * c_range * 1e-6)
        vdc_approx = Vout_peak - vr_approx / 2
        vdc_approx = np.clip(vdc_approx, 0, Vout_peak)
        vac_approx = vr_approx / (2 * np.sqrt(3))  # sawtooth approximation
        gamma_approx = np.where(vdc_approx > 0, vac_approx / vdc_approx, 0)

        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=c_range, y=gamma_approx,
            line=dict(color="#f0abfc", width=2.5),
            fill="tozeroy",
            fillcolor="#f0abfc14",
            name="Ripple Factor γ"
        ))
        if use_cap:
            fig3.add_vline(x=C, line=dict(color="#facc15", dash="dash", width=1.5),
                           annotation_text=f"  C = {C} µF", annotation_font_color="#facc15")
        fig3.update_layout(
            template="plotly_dark", paper_bgcolor="#0b0f1a", plot_bgcolor="#0d1520",
            height=260, margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(title="Capacitance C (µF)", gridcolor="#1a2a3a"),
            yaxis=dict(title="Ripple Factor γ", gridcolor="#1a2a3a"),
            font=dict(family="Share Tech Mono", color="#c0d4e8", size=10)
        )
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<p class="section-header">// Detailed Computed Parameters</p>', unsafe_allow_html=True)
    params_df = pd.DataFrame({
        "Parameter": [
            "Peak Input Voltage (Vₚ)", "RMS Input Voltage (Vᵢₙ_rms)",
            "Peak Output Voltage",     "DC Output Voltage (V_DC)",
            "RMS Output Voltage",      "Peak Inverse Voltage (PIV)",
            "DC Load Current (I_DC)",  "Peak Load Current (Iₚₑₐₖ)",
            "Ripple Voltage (Vᵣ p-p)", "Ripple Factor (γ)",
            "Rectifier Efficiency (η)","No. of Diodes"
        ],
        "Value": [
            f"{Vp:.2f} V",            f"{Vin_rms:.3f} V",
            f"{Vout_peak:.3f} V",     f"{Vout_dc:.3f} V",
            f"{Vout_rms:.3f} V",      f"{PIV:.2f} V",
            f"{Idc:.2f} mA",          f"{Ipeak:.2f} mA",
            f"{Vripple_pp:.4f} V",    f"{ripple_factor:.4f}",
            f"{eta:.2f} %",           str(n_diodes)
        ]
    })
    st.dataframe(params_df.set_index("Parameter"), use_container_width=True)

# ══════════════════════════════════════════════════════════
# TAB 4 — QUIZ
# ══════════════════════════════════════════════════════════
with tab4:
    st.markdown('<p class="section-header">// Viva-Voce Evaluation (6 Questions)</p>', unsafe_allow_html=True)
    st.info("Answer all six questions based on your observations from the Waveform Analyser tab, then submit.")

    CORRECT = {
        "q1": "0.636 Vₚ",
        "q2": "Both half-cycles of the AC input appear at the output",
        "q3": "It lowers the ripple factor by smoothing the output voltage",
        "q4": "PIV = 2Vₚ, making higher-rated diodes necessary",
        "q5": "0.482",
        "q6": "Ripple frequency doubles from the AC source frequency"
    }

    with st.form("viva_voce"):
        q1 = st.radio(
            "1. What is the theoretical DC output voltage of an ideal full-wave rectifier in terms of peak voltage Vₚ?",
            ["0.318 Vₚ", "0.636 Vₚ", "0.707 Vₚ", "Vₚ / 2"]
        )
        q2 = st.radio(
            "2. What fundamental advantage does a full-wave rectifier have over a half-wave rectifier?",
            [
                "It uses fewer diodes",
                "Both half-cycles of the AC input appear at the output",
                "It requires no transformer",
                "It produces a perfect DC output without filtering"
            ]
        )
        q3 = st.radio(
            "3. What is the role of the filter capacitor connected across the load?",
            [
                "It increases the peak output voltage",
                "It prevents current from flowing in the wrong direction",
                "It lowers the ripple factor by smoothing the output voltage",
                "It increases the rectifier efficiency"
            ]
        )
        q4 = st.radio(
            "4. What is the major disadvantage of the full-wave centre-tap rectifier compared to the bridge?",
            [
                "It requires four diodes instead of two",
                "PIV = 2Vₚ, making higher-rated diodes necessary",
                "It only rectifies one half-cycle",
                "It cannot be filtered with a capacitor"
            ]
        )
        q5 = st.radio(
            "5. The ripple factor (γ) of an unfiltered full-wave rectifier is approximately:",
            ["1.21", "0.707", "0.482", "0.318"]
        )
        q6 = st.radio(
            "6. Why is the output of a full-wave rectifier easier to filter than that of a half-wave rectifier?",
            [
                "Full-wave rectifiers have a higher peak voltage",
                "Ripple frequency doubles from the AC source frequency",
                "Full-wave rectifiers have zero ripple naturally",
                "The capacitor can be smaller and still block all DC"
            ]
        )

        submitted = st.form_submit_button("▶  SUBMIT EVALUATION")

    if submitted:
        answers = {"q1": q1, "q2": q2, "q3": q3, "q4": q4, "q5": q5, "q6": q6}
        score = sum(16 for k, v in answers.items() if v == CORRECT[k])
        # Round to 100 (6 questions × 16 = 96, give bonus for submitting)
        score = min(score + (4 if score == 96 else 0), 100)

        st.session_state["quiz_score"] = score
        st.session_state["quiz_submitted"] = True
        log_action(st.session_state["student_id"], "Quiz_Submission", f"Score={score}/100")

        if score >= 80:
            st.markdown(f"""
            <div class="quiz-result-pass">
                ✅  <strong>Score: {score} / 100</strong><br>
                Excellent performance. Your answers demonstrate solid understanding of rectification principles.
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="quiz-result-fail">
                ⚠️  <strong>Score: {score} / 100</strong><br>
                Review the Circuit Theory tab and re-examine your waveform data before re-attempting.
            </div>""", unsafe_allow_html=True)

        # Show correct answers breakdown
        with st.expander("📋 Answer Review"):
            for i, (k, correct_ans) in enumerate(CORRECT.items(), 1):
                user_ans = answers[k]
                icon = "✅" if user_ans == correct_ans else "❌"
                st.markdown(f"{icon} **Q{i}:** {correct_ans}")

st.markdown("---")
st.caption(f"⚡ Rectification Lab · Student: `{st.session_state['student_id']}` · Session active")