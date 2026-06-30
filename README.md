# ⚡ Rectification Lab

> **Interactive Half-Wave & Full-Wave Rectifier Simulator**  
> Department of Physics / Electronics — Power Electronics Laboratory

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?style=flat-square&logo=streamlit)
![Plotly](https://img.shields.io/badge/Plotly-5.x-3F4F75?style=flat-square&logo=plotly)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## Overview

**Rectification Lab** is a browser-based teaching instrument built with Streamlit and Plotly. Students simulate, observe, and analyse three rectifier topologies in real time — adjusting circuit parameters and watching waveforms, DC metrics, and ripple factor respond instantly. A six-question viva-voce quiz with auto-grading and a CSV analytics log complete the pedagogical workflow.

---

## Rectifier Topologies

| Topology | Diodes | V_DC (ideal) | Ripple Factor γ | Efficiency η | PIV | Centre-Tap? |
|---|---|---|---|---|---|---|
| **Half-Wave** | 1 | 0.318 Vₚ | 1.21 | 40.6 % | Vₚ | No |
| **Full-Wave — Centre-Tap** | 2 | 0.636 Vₚ | 0.482 | 81.2 % | 2Vₚ | **Required** |
| **Full-Wave — Bridge** | 4 | 0.636 Vₚ | 0.482 | 81.2 % | Vₚ | No |

---

## Features

- **Live waveform traces** — AC input overlay, rectified output, and post-filter signal on a single Plotly axis with DC level and ripple annotations  
- **RC filter simulation** — toggle a filter capacitor and watch ripple collapse in real time; a second subplot compares before and after  
- **Six live metric cards** — V_peak, V_DC, V_RMS, ripple factor γ, rectifier efficiency η, and PIV update on every slider move  
- **Circuit theory tab** — inline SVG schematics and key equations for every topology, plus a full comparative summary table  
- **Parametric sweep charts** — V_DC vs Vₚ and ripple factor vs capacitance C  
- **Auto-graded viva-voce quiz** — six multiple-choice questions, 0–100 score, pass/fail banner, per-question review  
- **Matriculation login & CSV analytics log** — every session, parameter change, and quiz score is timestamped and appended to `rectification_lab_log.csv`  
- **Waveform CSV export** — download the computed time-series data for offline analysis  

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/your-org/rectification-lab.git
cd rectification-lab

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
streamlit run rectification_lab.py
```

Open `http://localhost:8501`, enter your Matriculation Number, and begin.

---

## Requirements

```
streamlit>=1.30.0
numpy>=1.24.0
pandas>=2.0.0
plotly>=5.18.0
```

---

## Adjustable Parameters

| Parameter | Range | Default |
|---|---|---|
| Rectifier Topology | Half-Wave / FW Centre-Tap / FW Bridge | Half-Wave |
| Peak Voltage Vₚ | 1 – 50 V | 12 V |
| Frequency f | 10 – 500 Hz | 50 Hz |
| Diode Forward Drop Vd | 0.0 – 1.0 V | 0.7 V |
| Load Resistance Rₗ | 10 – 2000 Ω | 500 Ω |
| Filter Capacitance C | 1 – 10 000 µF | Off |
| AC Cycles Displayed | 1 – 6 | 3 |

---

## Project Structure

```
rectification-lab/
├── rectification_lab.py        # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── rectification_lab_log.csv   # Auto-generated analytics log (git-ignored)
└── .gitignore
```

---

## Analytics Log Schema

| Column | Description | Example |
|---|---|---|
| `Timestamp` | ISO datetime of the event | `2025-10-14 09:32:11` |
| `Student_ID` | Matriculation number | `ENG/2024/042` |
| `Action` | Event type | `Session_Start` · `Signal_Generated` · `Quiz_Submission` |
| `Details` | Action metadata | `Mode=Half-Wave, Vp=12, f=50, RL=500, C=0` |

> Add `rectification_lab_log.csv` to `.gitignore` to keep student data out of version control.

---

## Deployment

**Streamlit Community Cloud** — push to a public GitHub repo, connect at [share.streamlit.io](https://share.streamlit.io), set the main file to `rectification_lab.py`.

**Docker**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "rectification_lab.py", "--server.port=8080", "--server.address=0.0.0.0"]
```

**Local LAN / Lab Intranet**
```bash
streamlit run rectification_lab.py --server.address 0.0.0.0
```
Students connect via the host machine's IP on port `8501`.

---

## License

MIT License — free to use, modify, and distribute for educational or commercial purposes. See `LICENSE` for full terms.
