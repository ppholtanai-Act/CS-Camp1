import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PileForce Pro | เสาเข็มเยื้องศูนย์",
    page_icon="🪝",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;600;700;800&family=IBM+Plex+Mono:wght@400;600&display=swap');

:root {
  --bg:       #07090f;
  --surf:     #0e1219;
  --surf2:    #161c27;
  --surf3:    #1e2535;
  --border:   #2a3347;
  --accent:   #00d4ff;
  --accent2:  #0095b3;
  --gold:     #ffc544;
  --green:    #00e676;
  --red:      #ff5252;
  --orange:   #ff9100;
  --text:     #dce8f5;
  --muted:    #7a90aa;
  --radius:   10px;
}

html, body, [class*="css"] {
  font-family: 'Sarabun', sans-serif;
  background: var(--bg) !important;
  color: var(--text) !important;
}

.block-container { padding: 1.2rem 2rem 3rem; max-width: 1440px; }

/* HERO */
.hero {
  background: linear-gradient(120deg, #0e1a2e 0%, #07090f 60%, #0a1520 100%);
  border: 1px solid var(--border);
  border-left: 4px solid var(--accent);
  border-radius: var(--radius);
  padding: 1.8rem 2.2rem;
  margin-bottom: 1.5rem;
  position: relative; overflow: hidden;
}
.hero::after {
  content: ''; position: absolute; top: -60px; right: -60px;
  width: 220px; height: 220px;
  background: radial-gradient(circle, rgba(0,212,255,0.07) 0%, transparent 70%);
  border-radius: 50%;
}
.hero-eyebrow {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.65rem; letter-spacing: 3px;
  color: var(--accent); text-transform: uppercase; margin-bottom: 0.5rem;
}
.hero h1 {
  font-size: 2rem; font-weight: 800;
  color: var(--text); margin: 0 0 0.3rem; line-height: 1.15;
}
.hero h1 em { color: var(--accent); font-style: normal; }
.hero p { color: var(--muted); font-size: 0.9rem; margin: 0; }

/* CARD */
.card {
  background: var(--surf);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.2rem 1.5rem;
  margin-bottom: 0.9rem;
}
.card-hdr {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.65rem; letter-spacing: 2.5px;
  text-transform: uppercase; color: var(--accent);
  padding-bottom: 0.7rem; margin-bottom: 0.9rem;
  border-bottom: 1px solid var(--border);
  display: flex; align-items: center; gap: 0.5rem;
}

/* RESULT GRID */
.rg { display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 0.7rem; }
.rb {
  background: var(--surf2); border: 1px solid var(--border);
  border-radius: 8px; padding: 0.9rem 0.7rem; text-align: center;
}
.rb.accent { border-color: var(--accent); background: rgba(0,212,255,0.05); }
.rb.gold   { border-color: var(--gold);   background: rgba(255,197,68,0.05); }
.rb.safe   { border-color: var(--green);  background: rgba(0,230,118,0.05); }
.rb.warn   { border-color: var(--orange); background: rgba(255,145,0,0.05); }
.rb.danger { border-color: var(--red);    background: rgba(255,82,82,0.05); }
.rl { font-size: 0.65rem; color: var(--muted); letter-spacing: 1px; text-transform: uppercase; margin-bottom: 0.25rem; }
.rv { font-family: 'IBM Plex Mono', monospace; font-size: 1.3rem; font-weight: 600; color: var(--text); }
.ru { font-size: 0.65rem; color: var(--muted); margin-top: 0.15rem; }
.rb.accent .rv { color: var(--accent); }
.rb.gold   .rv { color: var(--gold); }
.rb.safe   .rv { color: var(--green); }
.rb.warn   .rv { color: var(--orange); }
.rb.danger .rv { color: var(--red); }

/* PILE TABLE */
.ptable { width: 100%; border-collapse: collapse; font-size: 0.84rem; }
.ptable th {
  background: var(--surf3); color: var(--muted);
  font-family: 'IBM Plex Mono', monospace; font-size: 0.65rem;
  letter-spacing: 1.5px; text-transform: uppercase;
  padding: 0.6rem 0.8rem; text-align: right; border-bottom: 2px solid var(--border);
}
.ptable th:first-child { text-align: center; }
.ptable td { padding: 0.55rem 0.8rem; text-align: right; border-bottom: 1px solid var(--surf2); }
.ptable td:first-child { text-align: center; font-weight: 600; color: var(--accent); font-family: 'IBM Plex Mono', monospace; }
.ptable tr:hover td { background: var(--surf2); }
.ptable .max-row td { color: var(--gold) !important; font-weight: 700; }
.ptable .min-row td { color: var(--green) !important; }
.ptable .danger-row td { color: var(--red) !important; font-weight: 700; }

/* BADGE */
.badge {
  display: inline-block; padding: 0.25rem 0.8rem;
  border-radius: 20px; font-size: 0.72rem; font-weight: 600;
  letter-spacing: 1px; text-transform: uppercase;
}
.b-safe   { background: rgba(0,230,118,0.12); color: var(--green);  border: 1px solid var(--green); }
.b-warn   { background: rgba(255,145,0,0.12);  color: var(--orange); border: 1px solid var(--orange); }
.b-danger { background: rgba(255,82,82,0.12);  color: var(--red);   border: 1px solid var(--red); }

.formula {
  background: #070b12; border: 1px solid var(--border);
  border-left: 3px solid var(--accent2);
  border-radius: 8px; padding: 0.9rem 1.1rem;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.8rem; color: #80c8e0; line-height: 1.8; margin: 0.5rem 0;
}

[data-testid="stSidebar"] {
  background: var(--surf) !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] label { color: var(--text) !important; font-size: 0.86rem !important; }
.stNumberInput > div > div > input {
  background: var(--surf2) !important; color: var(--text) !important;
  border-color: var(--border) !important;
}
.stSelectbox > div > div { background: var(--surf2) !important; border-color: var(--border) !important; }
div[data-baseweb="select"] { background: var(--surf2) !important; }
.stTabs [data-baseweb="tab"] { color: var(--muted) !important; font-family: 'Sarabun', sans-serif !important; }
.stTabs [aria-selected="true"] { color: var(--accent) !important; border-bottom-color: var(--accent) !important; }
hr { border-color: var(--border) !important; }
</style>
""", unsafe_allow_html=True)


# ─── Core Calculation Functions ───────────────────────────────────────────────

def get_pile_coords(layout, rows, cols, sx, sy):
    """สร้างตำแหน่งเสาเข็มตามรูปแบบ"""
    piles = []
    if layout == "ตารางสี่เหลี่ยม (Grid)":
        for i in range(rows):
            for j in range(cols):
                x = j * sx - (cols - 1) * sx / 2
                y = i * sy - (rows - 1) * sy / 2
                piles.append((x, y))
    elif layout == "แถวเดียว (Single Row)":
        for j in range(cols):
            x = j * sx - (cols - 1) * sx / 2
            piles.append((x, 0.0))
    elif layout == "สองแถว (Double Row)":
        for i in range(2):
            for j in range(cols):
                x = j * sx - (cols - 1) * sx / 2
                y = (i - 0.5) * sy
                piles.append((x, y))
    elif layout == "กำหนดเอง (Custom)":
        piles = None  # handled separately
    return piles


def calc_pile_forces(piles, P, Mx, My):
    """
    คำนวณแรงในเสาเข็มแต่ละต้น
    P_i = P/n + Mx·yi/Σyi² + My·xi/Σxi²
    """
    n = len(piles)
    xs = np.array([p[0] for p in piles])
    ys = np.array([p[1] for p in piles])

    sum_x2 = np.sum(xs ** 2)
    sum_y2 = np.sum(ys ** 2)

    forces = []
    for xi, yi in zip(xs, ys):
        fi = P / n
        if sum_y2 > 1e-9:
            fi += Mx * yi / sum_y2
        if sum_x2 > 1e-9:
            fi += My * xi / sum_x2
        forces.append(fi)
    return np.array(forces), xs, ys, sum_x2, sum_y2


def bearing_capacity_factors(phi_deg):
    phi = math.radians(phi_deg)
    if phi_deg == 0:
        return 5.7, 1.0, 0.0
    Kp = math.tan(math.radians(45) + phi / 2) ** 2
    Nq = math.exp(2 * math.pi * (0.75 - phi_deg / 360) * math.tan(phi)) / (
        2 * math.cos(math.radians(45 + phi_deg / 2)) ** 2)
    Nc = (Nq - 1) / math.tan(phi)
    Ng = (math.tan(phi) / 2) * (Kp / math.cos(phi) ** 2 - 1)
    return Nc, Nq, Ng


def pile_capacity(d, L_pile, c_avg, phi_deg, gamma, adhesion_factor=0.75):
    """กำลังรับแรงเสาเข็มเดี่ยว (Skin friction + End bearing)"""
    Nc, Nq, _ = bearing_capacity_factors(phi_deg)
    perimeter = math.pi * d
    area_tip  = math.pi * (d / 2) ** 2
    # Skin friction (alpha method)
    Qs = adhesion_factor * c_avg * perimeter * L_pile
    # End bearing (Terzaghi)
    qb = c_avg * Nc + gamma * L_pile * Nq
    Qb = qb * area_tip
    return Qs + Qb, Qs, Qb


# ─── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">🪝 Geotechnical · Pile Foundation Analysis v1.0</div>
  <h1>PileForce <em>Pro</em></h1>
  <p>ตรวจสอบแรงในกลุ่มเสาเข็มกรณีเยื้องศูนย์ (Eccentric Pile Group) — แรงตามแนวแกน + โมเมนต์ดัด (Mx, My)</p>
</div>
""", unsafe_allow_html=True)

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ พารามิเตอร์")
    st.markdown("---")

    st.markdown("### 🏗️ ผังเสาเข็ม")
    layout = st.selectbox("รูปแบบผัง", [
        "ตารางสี่เหลี่ยม (Grid)",
        "แถวเดียว (Single Row)",
        "สองแถว (Double Row)",
        "กำหนดเอง (Custom)"
    ])

    if layout != "กำหนดเอง (Custom)":
        if layout == "แถวเดียว (Single Row)":
            cols = st.number_input("จำนวนเสาเข็ม n", min_value=2, max_value=20, value=4, step=1)
            rows = 1
        elif layout == "สองแถว (Double Row)":
            cols = st.number_input("เสาต่อแถว", min_value=2, max_value=10, value=3, step=1)
            rows = 2
        else:
            cols = st.number_input("จำนวนคอลัมน์", min_value=1, max_value=8, value=3, step=1)
            rows = st.number_input("จำนวนแถว", min_value=1, max_value=8, value=3, step=1)
        sx = st.number_input("ระยะห่าง sx (m)", min_value=0.5, max_value=5.0, value=1.5, step=0.1)
        sy = st.number_input("ระยะห่าง sy (m)", min_value=0.5, max_value=5.0, value=1.5, step=0.1) if rows > 1 else 1.5
        piles = get_pile_coords(layout, rows, cols, sx, sy)
    else:
        st.markdown("**กรอกพิกัด x,y (เมตร) แต่ละต้น:**")
        raw = st.text_area("x,y ต่อบรรทัด", value="0,0\n1.5,0\n3,0\n0,1.5\n1.5,1.5\n3,1.5", height=150)
        piles = []
        for line in raw.strip().split("\n"):
            parts = line.strip().split(",")
            if len(parts) == 2:
                try:
                    piles.append((float(parts[0]), float(parts[1])))
                except:
                    pass

    n_piles = len(piles) if piles else 0

    st.markdown("### ⚡ แรงกระทำ")
    P  = st.number_input("แรงกด P (kN)", min_value=0.0, max_value=100000.0, value=2400.0, step=50.0)
    Mx = st.number_input("โมเมนต์ Mx (kN·m)", min_value=-5000.0, max_value=5000.0, value=300.0, step=10.0)
    My = st.number_input("โมเมนต์ My (kN·m)", min_value=-5000.0, max_value=5000.0, value=200.0, step=10.0)

    st.markdown("### 🪨 เสาเข็ม & ดิน")
    d_pile  = st.number_input("เส้นผ่าศูนย์กลาง d (m)", min_value=0.1, max_value=2.0, value=0.35, step=0.05)
    L_pile  = st.number_input("ความยาวเสาเข็ม L (m)", min_value=1.0, max_value=60.0, value=12.0, step=0.5)
    c_soil  = st.number_input("แรงยึดเกาะดิน c (kN/m²)", min_value=0.0, max_value=500.0, value=30.0, step=5.0)
    phi_s   = st.slider("มุมเสียดทาน φ (°)", 0, 40, 20)
    gamma_s = st.number_input("น้ำหนักดิน γ (kN/m³)", min_value=10.0, max_value=22.0, value=17.0, step=0.5)
    alpha   = st.slider("Adhesion factor α", 0.4, 1.0, 0.75, 0.05)

    st.markdown("### 🔒 ความปลอดภัย")
    FS = st.slider("Factor of Safety", 1.5, 4.0, 2.5, 0.5)

# ─── Calculations ─────────────────────────────────────────────────────────────
if not piles or n_piles < 2:
    st.warning("⚠️ กรุณากำหนดเสาเข็มอย่างน้อย 2 ต้น")
    st.stop()

forces, xs, ys, sum_x2, sum_y2 = calc_pile_forces(piles, P, Mx, My)
Qu, Qs_cap, Qb_cap = pile_capacity(d_pile, L_pile, c_soil, phi_s, gamma_s, alpha)
Qa = Qu / FS

max_f  = np.max(forces)
min_f  = np.min(forces)
max_idx = int(np.argmax(forces))
min_idx = int(np.argmin(forces))
ex = My / P if P > 1e-6 else 0
ey = Mx / P if P > 1e-6 else 0

# Status per pile
def pile_status(f, qa):
    if f < 0:
        return "ดึง", "warn"
    elif f > qa:
        return "เกิน", "danger"
    else:
        return "ปลอดภัย", "safe"

overall_ok  = all(f <= Qa for f in forces)
has_tension = any(f < 0 for f in forces)
if not overall_ok:
    ov_cls, ov_txt = "b-danger", "❌ ต้นที่เกินกำลัง"
elif has_tension:
    ov_cls, ov_txt = "b-warn", "⚠️ มีเสาเข็มรับแรงดึง"
else:
    ov_cls, ov_txt = "b-safe", "✅ ปลอดภัยทุกต้น"

# ─── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📊 ผลการคำนวณ", "📐 ผังเสาเข็ม", "📈 กราฟวิเคราะห์", "📋 ทฤษฎีและสูตร"])

# ══════════════════════════════════════════════════
# TAB 1 — Results
# ══════════════════════════════════════════════════
with tab1:
    col1, col2 = st.columns([3, 2], gap="medium")

    with col1:
        st.markdown(f"""
        <div class="card">
          <div class="card-hdr">⚡ แรงกระทำและความเยื้องศูนย์</div>
          <div class="rg">
            <div class="rb accent"><div class="rl">P รวม</div><div class="rv">{P:.0f}</div><div class="ru">kN</div></div>
            <div class="rb"><div class="rl">Mx</div><div class="rv">{Mx:.0f}</div><div class="ru">kN·m</div></div>
            <div class="rb"><div class="rl">My</div><div class="rv">{My:.0f}</div><div class="ru">kN·m</div></div>
            <div class="rb gold"><div class="rl">ex = My/P</div><div class="rv">{ex:.3f}</div><div class="ru">m</div></div>
            <div class="rb gold"><div class="rl">ey = Mx/P</div><div class="rv">{ey:.3f}</div><div class="ru">m</div></div>
            <div class="rb"><div class="rl">n เสาเข็ม</div><div class="rv">{n_piles}</div><div class="ru">ต้น</div></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Σxi², Σyi²
        st.markdown(f"""
        <div class="card">
          <div class="card-hdr">📐 ผลรวมกำลังสองระยะ</div>
          <div class="rg">
            <div class="rb"><div class="rl">Σxi²</div><div class="rv">{sum_x2:.3f}</div><div class="ru">m²</div></div>
            <div class="rb"><div class="rl">Σyi²</div><div class="rv">{sum_y2:.3f}</div><div class="ru">m²</div></div>
            <div class="rb"><div class="rl">P/n</div><div class="rv">{P/n_piles:.1f}</div><div class="ru">kN</div></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Pile table
        st.markdown('<div class="card"><div class="card-hdr">🔢 แรงในเสาเข็มแต่ละต้น</div>', unsafe_allow_html=True)
        rows_html = ""
        for i, (f, x, y) in enumerate(zip(forces, xs, ys)):
            st_txt, st_cls = pile_status(f, Qa)
            is_max = (i == max_idx)
            is_min = (i == min_idx)
            tr_cls = "max-row" if is_max else ("min-row" if is_min else "")
            if f > Qa:
                tr_cls = "danger-row"
            badge = f'<span class="badge b-{st_cls}">{st_txt}</span>'
            ratio = f / Qa * 100 if Qa > 0 else 0
            rows_html += f"""
            <tr class="{tr_cls}">
              <td>P{i+1}</td>
              <td>{x:.2f}</td><td>{y:.2f}</td>
              <td>{f:.2f}</td>
              <td>{Qa:.1f}</td>
              <td>{ratio:.1f}%</td>
              <td>{badge}</td>
            </tr>"""
        st.markdown(f"""
        <table class="ptable">
          <thead><tr>
            <th>เสาเข็ม</th><th>x (m)</th><th>y (m)</th>
            <th>Pi (kN)</th><th>Qa (kN)</th><th>%ใช้งาน</th><th>สถานะ</th>
          </tr></thead>
          <tbody>{rows_html}</tbody>
        </table>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        # Overall status
        st.markdown(f"""
        <div class="card" style="text-align:center;">
          <div class="card-hdr">✅ ผลการตรวจสอบรวม</div>
          <div style="font-size:3.5rem; margin: 0.5rem 0;">
            {'✅' if overall_ok and not has_tension else ('⚠️' if has_tension else '❌')}
          </div>
          <span class="badge {ov_cls}">{ov_txt}</span>
          <div style="margin-top:1.5rem; text-align:left;">
        """, unsafe_allow_html=True)

        util_max = max_f / Qa * 100 if Qa > 0 else 999
        bar_color = "var(--green)" if util_max <= 80 else ("var(--orange)" if util_max <= 100 else "var(--red)")
        st.markdown(f"""
            <div style="font-size:0.8rem; color:var(--muted); margin-bottom:0.3rem;">
              แรงสูงสุด P{max_idx+1} = {max_f:.1f} kN
            </div>
            <div style="background:var(--surf2); border-radius:6px; height:10px; overflow:hidden; margin-bottom:0.8rem;">
              <div style="width:{min(util_max,100):.1f}%; height:100%; background:{bar_color}; border-radius:6px;"></div>
            </div>
            <div style="font-size:0.75rem; color:var(--muted);">Utilization: {util_max:.1f}%</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Pile capacity
        Nc, Nq, Ng = bearing_capacity_factors(phi_s)
        st.markdown(f"""
        <div class="card">
          <div class="card-hdr">🪨 กำลังรับแรงเสาเข็ม (Terzaghi)</div>
          <div class="rg">
            <div class="rb"><div class="rl">Qu</div><div class="rv">{Qu:.0f}</div><div class="ru">kN</div></div>
            <div class="rb"><div class="rl">Qs (friction)</div><div class="rv">{Qs_cap:.0f}</div><div class="ru">kN</div></div>
            <div class="rb"><div class="rl">Qb (tip)</div><div class="rv">{Qb_cap:.0f}</div><div class="ru">kN</div></div>
            <div class="rb safe"><div class="rl">Qa=Qu/FS</div><div class="rv">{Qa:.0f}</div><div class="ru">kN</div></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Max/Min summary
        st.markdown(f"""
        <div class="card">
          <div class="card-hdr">🎯 ค่าสูงสุด-ต่ำสุด</div>
          <div class="rg">
            <div class="rb {'danger' if max_f > Qa else 'gold'}">
              <div class="rl">P_max (P{max_idx+1})</div>
              <div class="rv">{max_f:.1f}</div><div class="ru">kN</div>
            </div>
            <div class="rb safe">
              <div class="rl">P_min (P{min_idx+1})</div>
              <div class="rv">{min_f:.1f}</div><div class="ru">kN</div>
            </div>
            <div class="rb">
              <div class="rl">P_avg</div>
              <div class="rv">{np.mean(forces):.1f}</div><div class="ru">kN</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════
# TAB 2 — Pile Layout Diagram
# ══════════════════════════════════════════════════
with tab2:
    fig = go.Figure()

    # Color scale by force
    f_norm = (forces - min_f) / (max_f - min_f + 1e-9)
    colors_pile = [f"rgba({int(255*v)},{int(120*(1-v))},{int(200*(1-v))},0.9)" for v in f_norm]

    # Draw pile symbols
    for i, (x, y, f, col) in enumerate(zip(xs, ys, forces, colors_pile)):
        # Pile circle
        fig.add_shape(type="circle",
                      x0=x - 0.15, y0=y - 0.15, x1=x + 0.15, y1=y + 0.15,
                      fillcolor=col, line=dict(color="white", width=1.5))
        # Label
        fig.add_annotation(x=x, y=y + 0.28,
                           text=f"<b>P{i+1}</b><br>{f:.0f}kN",
                           showarrow=False,
                           font=dict(size=9, color="white", family="IBM Plex Mono"),
                           align="center")

    # Centroid
    cx = np.mean(xs)
    cy = np.mean(ys)

    # Eccentric load point
    load_x = cx + ex
    load_y = cy + ey

    fig.add_trace(go.Scatter(
        x=[cx], y=[cy], mode="markers",
        marker=dict(symbol="cross", size=14, color="#00d4ff", line=dict(width=2, color="white")),
        name="จุดศูนย์กลางเสาเข็ม"
    ))
    fig.add_trace(go.Scatter(
        x=[load_x], y=[load_y], mode="markers",
        marker=dict(symbol="star", size=16, color="#ffc544", line=dict(width=1.5, color="white")),
        name=f"จุดรับแรง (ex={ex:.2f}, ey={ey:.2f})"
    ))

    # Arrow from centroid to load point
    if abs(ex) > 0.01 or abs(ey) > 0.01:
        fig.add_annotation(
            x=load_x, y=load_y, ax=cx, ay=cy,
            xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=3, arrowwidth=2, arrowcolor="#ffc544"
        )

    # Cap outline (bounding box)
    x_min, x_max = xs.min() - 0.4, xs.max() + 0.4
    y_min, y_max = ys.min() - 0.4, ys.max() + 0.4
    fig.add_shape(type="rect", x0=x_min, y0=y_min, x1=x_max, y1=y_max,
                  fillcolor="rgba(0,212,255,0.03)",
                  line=dict(color="#2a3347", width=1.5, dash="dot"))

    fig.update_layout(
        title=dict(text="ผังเสาเข็มและการกระจายแรง", font=dict(color=="#dce8f5", size=15)),
        xaxis=dict(title="x (m)", gridcolor="#1e2535", zeroline=True, zerolinecolor="#2a3347",
                   scaleanchor="y", scaleratio=1),
        yaxis=dict(title="y (m)", gridcolor="#1e2535", zeroline=True, zerolinecolor="#2a3347"),
        paper_bgcolor="#0e1219", plot_bgcolor="#07090f",
        font=dict(color="#dce8f5", family="Sarabun"),
        legend=dict(bgcolor="#0e1219", bordercolor="#2a3347", x=0.01, y=0.99),
        height=520, margin=dict(t=50, b=40, l=50, r=30)
    )
    st.plotly_chart(fig, use_container_width=True)

    # Color scale legend
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:1rem; font-size:0.8rem; color:var(--muted); margin-top:-0.5rem;">
      <span style="color:var(--green);">■ แรงต่ำสุด {min_f:.1f} kN (P{min_idx+1})</span>
      <span>→</span>
      <span style="color:var(--red);">■ แรงสูงสุด {max_f:.1f} kN (P{max_idx+1})</span>
      <span>|</span>
      <span style="color:var(--accent);">✛ ศูนย์กลางกลุ่ม</span>
      <span style="color:var(--gold);">★ จุดรับแรง</span>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════
# TAB 3 — Charts
# ══════════════════════════════════════════════════
with tab3:
    c3a, c3b = st.columns(2)

    with c3a:
        # Bar chart of forces
        pile_labels = [f"P{i+1}" for i in range(n_piles)]
        bar_colors = ["#ff5252" if f > Qa else ("#ffc544" if i == max_idx else ("#00e676" if i == min_idx else "#00d4ff"))
                      for i, f in enumerate(forces)]
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=pile_labels, y=forces,
            marker_color=bar_colors,
            name="แรงในเสาเข็ม"
        ))
        fig_bar.add_hline(y=Qa, line_color="#00e676", line_dash="dash",
                          annotation_text=f"Qa={Qa:.0f}kN", annotation_font_color="#00e676")
        if any(f < 0 for f in forces):
            fig_bar.add_hline(y=0, line_color="#ffc544", line_dash="dot")
        fig_bar.update_layout(
            title="แรงในเสาเข็มแต่ละต้น",
            xaxis_title="เสาเข็ม", yaxis_title="Pi (kN)",
            paper_bgcolor="#0e1219", plot_bgcolor="#07090f",
            font=dict(color="#dce8f5", family="Sarabun"),
            xaxis=dict(gridcolor="#1e2535"), yaxis=dict(gridcolor="#1e2535"),
            height=360, margin=dict(t=50, b=40, l=50, r=20)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with c3b:
        # Sensitivity: force vs My
        My_range = np.linspace(-My * 3 if My > 0 else -500, My * 3 if My > 0 else 500, 80)
        f_max_list, f_min_list = [], []
        for myi in My_range:
            fi, *_ = calc_pile_forces(piles, P, Mx, myi)
            f_max_list.append(np.max(fi))
            f_min_list.append(np.min(fi))

        fig_sens = go.Figure()
        fig_sens.add_trace(go.Scatter(x=My_range, y=f_max_list, name="P_max",
                                      line=dict(color="#ff5252", width=2)))
        fig_sens.add_trace(go.Scatter(x=My_range, y=f_min_list, name="P_min",
                                      line=dict(color="#00e676", width=2)))
        fig_sens.add_hline(y=Qa, line_color="#ffc544", line_dash="dash",
                           annotation_text=f"Qa={Qa:.0f}kN", annotation_font_color="#ffc544")
        fig_sens.add_vline(x=My, line_color="#00d4ff", line_dash="dot",
                           annotation_text=f"My={My:.0f}", annotation_font_color="#00d4ff")
        fig_sens.update_layout(
            title="Sensitivity: แรงเสาเข็ม vs My",
            xaxis_title="My (kN·m)", yaxis_title="Pi (kN)",
            paper_bgcolor="#0e1219", plot_bgcolor="#07090f",
            font=dict(color="#dce8f5", family="Sarabun"),
            legend=dict(bgcolor="#0e1219", bordercolor="#2a3347"),
            xaxis=dict(gridcolor="#1e2535"), yaxis=dict(gridcolor="#1e2535"),
            height=360, margin=dict(t=50, b=40, l=50, r=20)
        )
        st.plotly_chart(fig_sens, use_container_width=True)

    # Heatmap of pile forces on grid
    if layout == "ตารางสี่เหลี่ยม (Grid)" and rows > 1 and cols > 1:
        try:
            grid_f = forces.reshape(rows, cols)
            fig_heat = go.Figure(data=go.Heatmap(
                z=grid_f,
                colorscale=[[0, "#00e676"], [0.5, "#00d4ff"], [1, "#ff5252"]],
                text=[[f"{v:.0f}" for v in row] for row in grid_f],
                texttemplate="%{text}",
                colorbar=dict(title="kN", tickfont=dict(color="#dce8f5"))
            ))
            fig_heat.update_layout(
                title="Heatmap แรงในเสาเข็ม",
                paper_bgcolor="#0e1219", plot_bgcolor="#07090f",
                font=dict(color="#dce8f5", family="Sarabun"),
                height=320, margin=dict(t=50, b=40, l=50, r=20)
            )
            st.plotly_chart(fig_heat, use_container_width=True)
        except:
            pass

# ══════════════════════════════════════════════════
# TAB 4 — Theory
# ══════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="card"><div class="card-hdr">📚 ทฤษฎีเสาเข็มเยื้องศูนย์</div>', unsafe_allow_html=True)
    st.markdown("""
    เมื่อแรงกระทำไม่ผ่านจุดศูนย์กลางของกลุ่มเสาเข็ม (Eccentric Loading) จะเกิดโมเมนต์ดัด Mx และ My
    ทำให้แรงในเสาเข็มแต่ละต้นไม่เท่ากัน การวิเคราะห์ใช้หลักการ Elastic Method (Rigid Cap Assumption)
    """)
    st.markdown("""
    <div class="formula">
สูตรแรงในเสาเข็มที่ i (Elastic Method):

  Pi = P/n  +  (Mx · yi) / Σyi²  +  (My · xi) / Σxi²

เมื่อ:
  Pi   = แรงในเสาเข็มต้นที่ i (kN)
  P    = แรงกดรวมที่ฐานรากรับ (kN)
  n    = จำนวนเสาเข็มทั้งหมด (ต้น)
  Mx   = โมเมนต์ดัดรอบแกน X (kN·m)
  My   = โมเมนต์ดัดรอบแกน Y (kN·m)
  xi, yi = ระยะของเสาเข็ม i จากจุดศูนย์กลางกลุ่ม (m)
  Σxi² = ผลรวมกำลังสองระยะในแนว X ทุกต้น (m²)
  Σyi² = ผลรวมกำลังสองระยะในแนว Y ทุกต้น (m²)

ความเยื้องศูนย์:
  ex = My / P    (ระยะเยื้องในแนว X)
  ey = Mx / P    (ระยะเยื้องในแนว Y)

เงื่อนไขความปลอดภัย:
  Pi_max ≤ Qa = Qu / FS
  Pi_min ≥ 0  (ถ้า Pi < 0 เสาเข็มรับแรงดึง ต้องตรวจสอบ)
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="card-hdr" style="margin-top:1.2rem;">🪨 กำลังรับแรงเสาเข็มเดี่ยว (Terzaghi Alpha Method)</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="formula">
กำลังรับแรงเสาเข็มรวม:
  Qu = Qs + Qb

แรงเสียดทานข้างเสาเข็ม (Skin Friction — α method):
  Qs = α · c · As = α · c · (π·d·L)

แรงต้านที่ปลายเสาเข็ม (End Bearing — Terzaghi):
  Qb = (c·Nc + γ·L·Nq) · Ab   ;   Ab = π(d/2)²

กำลังรับแรงที่ยอมให้:
  Qa = Qu / FS    (FS แนะนำ 2.5)
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Summary table
    st.markdown(f"""
    <div class="card">
      <div class="card-hdr">📊 สรุปผลการคำนวณ</div>
      <table class="ptable">
        <tr><td style="text-align:left; color:var(--muted);">จำนวนเสาเข็ม n</td><td>{n_piles} ต้น</td></tr>
        <tr><td style="text-align:left; color:var(--muted);">แรงกด P</td><td>{P:.0f} kN</td></tr>
        <tr><td style="text-align:left; color:var(--muted);">Mx / My</td><td>{Mx:.0f} / {My:.0f} kN·m</td></tr>
        <tr><td style="text-align:left; color:var(--muted);">ex / ey</td><td>{ex:.3f} / {ey:.3f} m</td></tr>
        <tr><td style="text-align:left; color:var(--muted);">Σxi² / Σyi²</td><td>{sum_x2:.3f} / {sum_y2:.3f} m²</td></tr>
        <tr><td style="text-align:left; color:var(--muted);">Qu / Qa (FS={FS})</td><td>{Qu:.0f} / {Qa:.0f} kN</td></tr>
        <tr><td style="text-align:left; color:var(--muted);">Pi_max (P{max_idx+1})</td><td style="color:{'var(--red)' if max_f > Qa else 'var(--gold)'};">{max_f:.1f} kN</td></tr>
        <tr><td style="text-align:left; color:var(--muted);">Pi_min (P{min_idx+1})</td><td style="color:{'var(--orange)' if min_f < 0 else 'var(--green)'};">{min_f:.1f} kN</td></tr>
        <tr><td style="text-align:left; color:var(--muted);">สถานะ</td><td><span class="badge {ov_cls}">{ov_txt}</span></td></tr>
      </table>
    </div>
    """, unsafe_allow_html=True)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; color:var(--muted); font-size:0.75rem; margin-top:3rem;
            padding-top:1rem; border-top:1px solid var(--border);">
  <span style="font-family:'IBM Plex Mono'; color:var(--accent);">PileForce Pro</span> —
  อ้างอิง: Terzaghi (1943) · Elastic Pile Group Method · Das, B.M. <em>Principles of Foundation Engineering</em><br>
  พัฒนาเพื่อการศึกษาและงานวิศวกรรมปฐพี
</div>
""", unsafe_allow_html=True)
