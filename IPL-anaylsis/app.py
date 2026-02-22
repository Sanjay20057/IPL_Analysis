import streamlit as st
import pandas as pd
import helper
import plotly.express as px
import plotly.graph_objects as go

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IPL Analytics",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── MASTER CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Bebas+Neue&family=DM+Mono:wght@400;500&display=swap');

:root {
  --bg-base:       #04040a;
  --bg-surface:    #080812;
  --bg-card:       rgba(255,255,255,0.04);
  --border:        rgba(255,255,255,0.08);
  --border-glow:   rgba(255,136,0,0.35);
  --neon-orange:   #ff8800;
  --neon-gold:     #ffd700;
  --neon-red:      #ff3366;
  --text-primary:  #f0f0f8;
  --text-muted:    #5a5a7a;
  --text-dim:      #2a2a42;
  --font-display:  'Bebas Neue', sans-serif;
  --font-body:     'Outfit', sans-serif;
  --font-mono:     'DM Mono', monospace;
  --radius-sm:     8px;
  --radius-md:     14px;
  --radius-lg:     20px;
  --glow-orange:   0 0 30px rgba(255,136,0,0.25), 0 0 60px rgba(255,136,0,0.1);
}

/* ── Background ── */
.stApp {
  background: var(--bg-base);
  font-family: var(--font-body);
  color: var(--text-primary);
}
.stApp::before {
  content: '';
  position: fixed;
  inset: 0;
  background:
    radial-gradient(ellipse 80% 50% at 20% -10%, rgba(255,136,0,0.08) 0%, transparent 60%),
    radial-gradient(ellipse 60% 40% at 80% 110%, rgba(255,51,102,0.06) 0%, transparent 60%),
    radial-gradient(ellipse 50% 60% at 50% 50%, rgba(255,215,0,0.03) 0%, transparent 70%);
  pointer-events: none;
  z-index: -1;
  animation: bgPulse 8s ease-in-out infinite alternate;
}
@keyframes bgPulse { 0%{opacity:.7} 100%{opacity:1} }

.stApp::after {
  content: '';
  position: fixed;
  width: 600px; height: 600px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255,136,0,0.04) 0%, transparent 70%);
  top: -200px; right: -200px;
  animation: orbFloat 12s ease-in-out infinite alternate;
  pointer-events: none;
  z-index: -1;
}
@keyframes orbFloat {
  0%   { transform: translate(0,0) scale(1); }
  100% { transform: translate(-100px,100px) scale(1.2); }
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: rgba(4,4,10,0.97) !important;
  border-right: 1px solid var(--border) !important;
  backdrop-filter: blur(20px);
}
.sb-brand {
  font-family: var(--font-display);
  font-size: 2.4rem;
  letter-spacing: 0.12em;
  line-height: 1;
  background: linear-gradient(135deg, #ff8800 0%, #ffd700 50%, #ff8800 100%);
  background-size: 200%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: brandShimmer 4s linear infinite;
  padding: 0 1rem;
}
@keyframes brandShimmer { 0%{background-position:0%} 100%{background-position:200%} }
.sb-tagline {
  font-size: 0.62rem;
  color: var(--text-muted);
  letter-spacing: 0.2em;
  text-transform: uppercase;
  font-family: var(--font-mono);
  padding: 0 1rem;
  margin-top: 2px;
  margin-bottom: 1rem;
}
.sb-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,136,0,0.3), transparent);
  margin: 0.75rem 0;
}
.sb-nav-label {
  font-size: 0.58rem;
  color: var(--text-dim);
  letter-spacing: 0.25em;
  text-transform: uppercase;
  font-family: var(--font-mono);
  padding: 0 1rem;
  margin-bottom: 0.5rem;
}

/* Radio overrides */
[data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p {
  font-family: var(--font-body) !important;
  font-size: 0.88rem !important;
  font-weight: 500 !important;
  color: #6a6a8a !important;
  letter-spacing: 0.03em;
}

/* Selectbox */
[data-testid="stSelectbox"] > div > div {
  background: rgba(255,255,255,0.03) !important;
  border: 1px solid rgba(255,136,0,0.2) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--text-primary) !important;
  font-family: var(--font-body) !important;
  transition: border-color 0.2s, box-shadow 0.2s;
}
[data-testid="stSelectbox"] > div > div:hover {
  border-color: rgba(255,136,0,0.5) !important;
  box-shadow: 0 0 15px rgba(255,136,0,0.1) !important;
}

/* ── Main container ── */
.main .block-container {
  padding: 2rem 2.5rem 3rem;
  max-width: 1400px;
  position: relative;
  z-index: 1;
}
@media (max-width: 768px) {
  .main .block-container { padding: 1.25rem 1rem 2rem; }
}

/* ── Page header ── */
.ph-wrap {
  position: relative;
  margin-bottom: 2.5rem;
  padding-bottom: 1.5rem;
}
.ph-eyebrow {
  font-family: var(--font-mono);
  font-size: 0.62rem;
  color: #ff8800;
  letter-spacing: 0.3em;
  text-transform: uppercase;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.ph-eyebrow::before {
  content: '';
  display: inline-block;
  width: 20px; height: 1px;
  background: #ff8800;
}
.ph-title {
  font-family: var(--font-display);
  font-size: clamp(3rem, 6vw, 5rem);
  letter-spacing: 0.05em;
  line-height: 0.9;
  color: var(--text-primary);
  margin: 0;
}
.ph-title .hl {
  background: linear-gradient(90deg, #ff8800, #ffd700);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.ph-underline {
  position: absolute;
  bottom: 0; left: 0;
  width: 60px; height: 2px;
  background: linear-gradient(90deg, #ff8800, #ffd700);
  border-radius: 2px;
  box-shadow: var(--glow-orange);
}

/* ── KPI Cards ── */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 1rem;
  margin-bottom: 2.5rem;
}
.kpi-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 1.4rem 1.6rem;
  position: relative;
  overflow: hidden;
  transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
  cursor: default;
}
.kpi-card:hover {
  transform: translateY(-3px);
  border-color: var(--border-glow);
  box-shadow: var(--glow-orange);
}
.kpi-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(255,136,0,0.06) 0%, transparent 60%);
  opacity: 0;
  transition: opacity 0.3s;
}
.kpi-card:hover::before { opacity: 1; }
.kpi-icon  { font-size: 1.3rem; margin-bottom: 0.7rem; }
.kpi-val {
  font-family: var(--font-display);
  font-size: 2.4rem;
  letter-spacing: 0.04em;
  line-height: 1;
  background: linear-gradient(90deg, #ff8800, #ffd700);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.kpi-lbl {
  font-family: var(--font-mono);
  font-size: 0.6rem;
  color: var(--text-muted);
  letter-spacing: 0.15em;
  text-transform: uppercase;
  margin-top: 0.3rem;
}
.kpi-bar {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, #ff8800, #ffd700, transparent);
}

/* ── Section label ── */
.sl {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin: 1.75rem 0 0.6rem;
}
.sl-dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: #ff8800;
  box-shadow: 0 0 10px #ff8800;
  flex-shrink: 0;
}
.sl-text {
  font-family: var(--font-mono);
  font-size: 0.62rem;
  color: var(--text-muted);
  letter-spacing: 0.2em;
  text-transform: uppercase;
}
.sl-line {
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, rgba(255,136,0,0.2), transparent);
}

/* ── Divider strip ── */
.strip {
  width: 100%;
  height: 1px;
  background: linear-gradient(90deg, transparent 0%, rgba(255,136,0,0.4) 30%, rgba(255,215,0,0.4) 60%, transparent 100%);
  margin: 2.5rem 0 2rem;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
  border-radius: var(--radius-md) !important;
  overflow: hidden;
  border: 1px solid var(--border) !important;
}
[data-testid="stDataFrame"] th {
  background: rgba(255,136,0,0.08) !important;
  color: #ff8800 !important;
  font-family: var(--font-mono) !important;
  font-size: 0.68rem !important;
  letter-spacing: 0.12em !important;
  text-transform: uppercase !important;
  border-bottom: 1px solid var(--border-glow) !important;
}
[data-testid="stDataFrame"] td {
  color: var(--text-primary) !important;
  font-family: var(--font-body) !important;
  font-size: 0.85rem !important;
  border-color: var(--border) !important;
}

/* ── Chart hover glow ── */
[data-testid="stPlotlyChart"] > div {
  border-radius: var(--radius-lg) !important;
  border: 1px solid var(--border);
  transition: border-color 0.3s, box-shadow 0.3s;
}
[data-testid="stPlotlyChart"] > div:hover {
  border-color: rgba(255,136,0,0.2);
  box-shadow: 0 8px 40px rgba(0,0,0,0.4), 0 0 30px rgba(255,136,0,0.06);
}

/* ── Landing page ── */
.hero {
  min-height: 45vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 3rem 1rem 2rem;
}
.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255,136,0,0.08);
  border: 1px solid rgba(255,136,0,0.25);
  color: #ff8800;
  font-family: var(--font-mono);
  font-size: 0.62rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  padding: 0.5rem 1.2rem;
  border-radius: 999px;
  margin-bottom: 2rem;
  animation: fadeInDown 0.6s ease both;
}
.hero-badge::before {
  content: '';
  width: 6px; height: 6px;
  border-radius: 50%;
  background: #ff8800;
  box-shadow: 0 0 8px #ff8800;
}
.hero-h1 {
  font-family: var(--font-display);
  font-size: clamp(5rem, 12vw, 10rem);
  letter-spacing: 0.06em;
  line-height: 0.85;
  margin-bottom: 0.5rem;
  animation: fadeInUp 0.7s ease 0.1s both;
}
.hero-h1 .line1 { color: var(--text-primary); }
.hero-h1 .line2 {
  background: linear-gradient(90deg, #ff8800 0%, #ffd700 40%, #ff3366 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: block;
}
.hero-season {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  color: var(--text-muted);
  letter-spacing: 0.3em;
  margin-bottom: 2.5rem;
  animation: fadeInUp 0.7s ease 0.2s both;
}
.hero-desc {
  max-width: 500px;
  margin: 0 auto 3rem;
  color: #4a4a6a;
  font-size: 1rem;
  line-height: 1.8;
  animation: fadeInUp 0.7s ease 0.3s both;
}
.hero-arrow {
  font-family: var(--font-mono);
  font-size: 0.65rem;
  color: rgba(255,136,0,0.5);
  letter-spacing: 0.2em;
  animation: fadeInUp 0.7s ease 0.4s both, arrowBlink 2s ease-in-out infinite;
}
@keyframes arrowBlink { 0%,100%{opacity:.4} 50%{opacity:1} }

@keyframes fadeInDown {
  from { opacity:0; transform:translateY(-20px); }
  to   { opacity:1; transform:translateY(0); }
}
@keyframes fadeInUp {
  from { opacity:0; transform:translateY(30px); }
  to   { opacity:1; transform:translateY(0); }
}

.feat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1px;
  background: var(--border);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  max-width: 960px;
  margin: 2rem auto 0;
  animation: fadeInUp 0.8s ease 0.5s both;
}
.feat-item {
  background: var(--bg-surface);
  padding: 1.75rem;
  transition: background 0.2s;
  position: relative;
}
.feat-item:hover { background: rgba(255,136,0,0.04); }
.feat-item:hover .feat-icon { transform: scale(1.15) rotate(-5deg); }
.feat-icon {
  font-size: 2rem;
  display: block;
  margin-bottom: 1rem;
  transition: transform 0.3s;
}
.feat-name {
  font-family: var(--font-display);
  font-size: 1.1rem;
  letter-spacing: 0.05em;
  color: var(--text-primary);
  margin-bottom: 0.4rem;
}
.feat-desc {
  font-size: 0.78rem;
  color: var(--text-muted);
  line-height: 1.6;
}
.feat-num {
  position: absolute;
  top: 1.25rem; right: 1.25rem;
  font-family: var(--font-mono);
  font-size: 0.58rem;
  color: var(--text-dim);
  letter-spacing: 0.1em;
}

@media (max-width: 640px) {
  .kpi-grid { grid-template-columns: 1fr 1fr; }
  .hero-h1  { font-size: 4.5rem; }
  .feat-grid { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 400px) {
  .feat-grid { grid-template-columns: 1fr; }
}
</style>
""", unsafe_allow_html=True)

# ─── DATA ─────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    d = pd.read_csv('IPL-anaylsis/deliveries(1).csv')
    m = pd.read_csv('IPL-anaylsis/matches(1).csv')
    return d, m

Deliveries, Matches = load_data()

# ─── PLOTLY THEME ─────────────────────────────────────────────────────────────
T = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Outfit', color='#5a5a7a', size=12),
    title_font=dict(family='Bebas Neue', size=22, color='#f0f0f8'),
    xaxis=dict(
        gridcolor='rgba(255,255,255,0.04)',
        linecolor='rgba(255,255,255,0.06)',
        tickcolor='rgba(255,255,255,0.06)',
        tickfont=dict(size=10, color='#5a5a7a'),
        title_font=dict(size=11, color='#5a5a7a'),
    ),
    yaxis=dict(
        gridcolor='rgba(255,255,255,0.04)',
        linecolor='rgba(255,255,255,0.06)',
        tickcolor='rgba(255,255,255,0.06)',
        tickfont=dict(size=10, color='#5a5a7a'),
        title_font=dict(size=11, color='#5a5a7a'),
    ),
    colorway=['#ff8800','#ffd700','#ff3366','#00d4ff','#a855f7','#22c55e'],
    margin=dict(l=20, r=20, t=55, b=30),
    legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#5a5a7a', size=11)),
    hoverlabel=dict(
        bgcolor='rgba(8,8,18,0.97)',
        bordercolor='rgba(255,136,0,0.4)',
        font=dict(family='Outfit', size=12, color='#f0f0f8'),
    ),
)
CSCALE  = [[0,'#0a0a18'],[0.5,'#ff8800'],[1,'#ffd700']]
CSCALE2 = [[0,'#0a0a18'],[1,'#ff3366']]

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def page_header(eyebrow, title, accent):
    st.markdown(f"""
    <div class="ph-wrap">
      <div class="ph-eyebrow">{eyebrow}</div>
      <div class="ph-title">{title} <span class="hl">{accent}</span></div>
      <div class="ph-underline"></div>
    </div>""", unsafe_allow_html=True)

def section_label(text):
    st.markdown(f"""
    <div class="sl">
      <div class="sl-dot"></div>
      <div class="sl-text">{text}</div>
      <div class="sl-line"></div>
    </div>""", unsafe_allow_html=True)

def kpi(icon, val, lbl):
    return f"""<div class="kpi-card">
      <div class="kpi-icon">{icon}</div>
      <div class="kpi-val">{val}</div>
      <div class="kpi-lbl">{lbl}</div>
      <div class="kpi-bar"></div>
    </div>"""

def tfig(fig, title=''):
    fig.update_layout(**T)
    fig.update_layout(height=500)
    if title:
        fig.update_layout(title=dict(text=title))
    return fig

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding-top:1.5rem">
      <div class="sb-brand">IPL HUB</div>
      <div class="sb-tagline">Analytics · 2008–2019</div>
      <div class="sb-divider"></div>
      <div class="sb-nav-label">Navigation</div>
    </div>""", unsafe_allow_html=True)

    user_menu = st.radio('', [
        '⬡  Home',
        '◈  Most Played Team',
        '◉  Season Winner',
        '▷  Batsman',
        '◎  Bowler',
        '◆  Boundaries',
        '▣  Batsman Score',
        '●  Orange Cap',
    ], label_visibility='collapsed')

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
    st.image(
        'https://files.ekmcdn.com/aswanicricket/images/2024-tata-ipl-ranges-510-c.gif?w=400&h=400&v=306D7880-3039-4F01-997D-E3EEA8E7C83F',
        width=160
    )
    st.markdown("""
    <div style="font-family:'DM Mono',monospace;font-size:0.58rem;color:#2a2a42;text-align:center;margin-top:0.5rem;letter-spacing:0.15em">
      TATA IPL · T20 CRICKET
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  HOME
# ══════════════════════════════════════════════════════════════════════════════
if user_menu == '⬡  Home':
    st.markdown("""
    <div class="hero">
      <div class="hero-badge">Indian Premier League · Data Hub</div>
      <div class="hero-h1">
        <span class="line1">CRICKET</span>
        <span class="line2">ANALYTICS</span>
      </div>
      <div class="hero-season">SEASONS 2008 — 2019</div>
      <div class="hero-desc">
        12 seasons of T20 excellence decoded. Explore every boundary,
        title, and record from the world's most electrifying cricket league.
      </div>
      <div class="hero-arrow">← USE SIDEBAR TO NAVIGATE →</div>
    </div>""", unsafe_allow_html=True)

    n_matches  = len(Matches)
    n_seasons  = Matches['season'].nunique()
    n_players  = Deliveries['batsman'].nunique()
    n_balls    = len(Deliveries)
    total_runs = int(Deliveries['total_runs'].sum())
    n_teams    = Matches['team1'].nunique()

    st.markdown(f"""
    <div class="kpi-grid">
      {kpi('🏟️', n_matches,   'Total Matches')}
      {kpi('📅', n_seasons,   'Seasons')}
      {kpi('🏏', n_players,   'Batsmen')}
      {kpi('⚾', f'{n_balls:,}',    'Deliveries')}
      {kpi('🔥', f'{total_runs:,}', 'Runs Scored')}
      {kpi('🛡️', n_teams,    'Teams')}
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="strip"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="feat-grid">
      <div class="feat-item"><span class="feat-num">01</span>
        <span class="feat-icon">🏟️</span>
        <div class="feat-name">Most Played</div>
        <div class="feat-desc">Teams ranked by total matches across all seasons.</div>
      </div>
      <div class="feat-item"><span class="feat-num">02</span>
        <span class="feat-icon">🏆</span>
        <div class="feat-name">Champions</div>
        <div class="feat-desc">Season winners and title counts by franchise.</div>
      </div>
      <div class="feat-item"><span class="feat-num">03</span>
        <span class="feat-icon">🏏</span>
        <div class="feat-name">Batsmen</div>
        <div class="feat-desc">Career runs, top scorers &amp; per-season leaders.</div>
      </div>
      <div class="feat-item"><span class="feat-num">04</span>
        <span class="feat-icon">🎯</span>
        <div class="feat-name">Bowlers</div>
        <div class="feat-desc">Economy rates, wickets &amp; runs conceded data.</div>
      </div>
      <div class="feat-item"><span class="feat-num">05</span>
        <span class="feat-icon">💥</span>
        <div class="feat-name">Boundaries</div>
        <div class="feat-desc">Fours &amp; sixes breakdowns by player and match.</div>
      </div>
      <div class="feat-item"><span class="feat-num">06</span>
        <span class="feat-icon">🟠</span>
        <div class="feat-name">Orange Cap</div>
        <div class="feat-desc">Season-by-season highest run scorer tracker.</div>
      </div>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  MOST PLAYED TEAM
# ══════════════════════════════════════════════════════════════════════════════
elif user_menu == '◈  Most Played Team':
    page_header('Team Statistics', 'Most Played', 'Teams')

    MPT = helper.Most_Played_Team(Matches)
    top = MPT.iloc[0]

    st.markdown(f"""
    <div class="kpi-grid">
      {kpi('🥇', top['Matches Played'], 'Most Games · '+top['Team'])}
      {kpi('🏟️', len(MPT),             'Total Teams')}
      {kpi('📊', int(MPT['Matches Played'].mean()), 'Avg Matches')}
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 2], gap='large')
    with col1:
        section_label('Data Table')
        st.dataframe(MPT, use_container_width=True, hide_index=True)
    with col2:
        section_label('Bar Chart')
        fig = px.bar(MPT, x='Team', y='Matches Played', text='Matches Played',
                     color='Matches Played', color_continuous_scale=CSCALE)
        fig.update_traces(texttemplate='%{text}', textposition='outside',
                          textfont=dict(size=10, color='#5a5a7a'), marker_line_width=0)
        tfig(fig, 'MATCHES PER TEAM')
        fig.update_layout(coloraxis_showscale=False, xaxis_tickangle=-40)
        st.plotly_chart(fig, use_container_width=True)

    section_label('Trend Line')
    fig2 = px.line(MPT, x='Team', y='Matches Played', markers=True)
    fig2.update_traces(
        line=dict(color='#ff8800', width=2.5),
        marker=dict(color='#ffd700', size=9, line=dict(color='#ff8800', width=2)),
        fill='tozeroy', fillcolor='rgba(255,136,0,0.06)'
    )
    tfig(fig2, 'PARTICIPATION TREND')
    fig2.update_xaxes(tickangle=-40)
    st.plotly_chart(fig2, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
#  SEASON WINNER
# ══════════════════════════════════════════════════════════════════════════════
elif user_menu == '◉  Season Winner':
    page_header('Championship', 'Season', 'Winners')

    season_list, winner_list = helper.Season_Winner(Matches)
    col1, col2 = st.columns(2, gap='medium')
    with col1: Selected_season = st.selectbox('Season', season_list)
    with col2: Selected_winner = st.selectbox('Team',   winner_list)

    SW = helper.fetch_Season_Winner(Matches, Selected_season, Selected_winner)
    st.dataframe(SW, use_container_width=True, hide_index=True)
    st.markdown('<div class="strip"></div>', unsafe_allow_html=True)

    sdf = Matches.drop_duplicates('season', keep='last')[['season','winner']].sort_values('season').reset_index(drop=True)

    col1, col2 = st.columns(2, gap='large')
    with col1:
        section_label('Season by Season')
        fig = px.bar(sdf, x='season', y='winner', text='winner',
                     color_discrete_sequence=['#ff8800'])
        fig.update_traces(textangle=0, textposition='outside',
                          textfont=dict(size=9, color='#5a5a7a'), marker_line_width=0)
        tfig(fig, 'CHAMPIONS EACH SEASON')
        fig.update_xaxes(tickangle=-40)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section_label('Title Count')
        wc = sdf['winner'].value_counts().reset_index()
        wc.columns = ['Team','Titles']
        fig2 = px.bar(wc, x='Team', y='Titles', text='Titles',
                      color='Titles', color_continuous_scale=CSCALE)
        fig2.update_traces(texttemplate='%{text}', textposition='outside', marker_line_width=0)
        tfig(fig2, 'TITLES WON BY TEAM')
        fig2.update_layout(coloraxis_showscale=False, xaxis_tickangle=-40)
        st.plotly_chart(fig2, use_container_width=True)

    section_label('Title Share — Donut')
    wc2 = sdf['winner'].value_counts().reset_index()
    wc2.columns = ['Team','Titles']
    fig3 = go.Figure(go.Pie(
        labels=wc2['Team'], values=wc2['Titles'], hole=0.6,
        textinfo='label+percent',
        textfont=dict(family='Outfit', size=11, color='#f0f0f8'),
        marker=dict(
            colors=['#ff8800','#ffd700','#ff3366','#00d4ff','#a855f7','#22c55e','#f97316','#ec4899'],
            line=dict(color='#04040a', width=3)
        )
    ))
    fig3.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Outfit', color='#5a5a7a'),
        height=500,
        annotations=[dict(text='🏆', x=0.5, y=0.5, font_size=28, showarrow=False)]
    )
    fig3.update_layout(title=dict(text='TITLE SHARE'))
    st.plotly_chart(fig3, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
#  BATSMAN
# ══════════════════════════════════════════════════════════════════════════════
elif user_menu == '▷  Batsman':
    page_header('Batting Records', 'Top', 'Batsmen')

    batsman_list = helper.Batsman_Run(Deliveries)
    Selected_batsman = st.selectbox('Select Batsman', batsman_list)
    Batsman_df = helper.fetch_Batsman_Run(Deliveries, Selected_batsman)
    st.dataframe(Batsman_df, use_container_width=True, hide_index=True)

    Runs  = Deliveries.groupby("batsman")['batsman_runs'].sum().sort_values(ascending=False)
    Top25 = Runs.head(25).reset_index()
    Top25.columns = ['Batsman','Total Runs']
    tb = Top25.iloc[0]

    st.markdown(f"""
    <div class="kpi-grid">
      {kpi('👑', tb['Total Runs'],           'Most Runs · '+tb['Batsman'])}
      {kpi('📊', len(batsman_list)-1,        'Total Batsmen')}
      {kpi('🔥', int(Top25['Total Runs'].mean()), 'Avg (Top 25)')}
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap='large')
    with col1:
        section_label('Vertical Bar')
        fig = px.bar(Top25, x='Batsman', y='Total Runs', text='Total Runs',
                     color='Total Runs', color_continuous_scale=CSCALE)
        fig.update_traces(texttemplate='%{text:.2s}', textposition='outside',
                          textfont=dict(size=9,color='#5a5a7a'), marker_line_width=0)
        tfig(fig, 'TOP 25 RUN SCORERS')
        fig.update_layout(coloraxis_showscale=False, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section_label('Horizontal Rank')
        fig2 = px.bar(Top25.sort_values('Total Runs'), y='Batsman', x='Total Runs',
                      text='Total Runs', orientation='h',
                      color='Total Runs', color_continuous_scale=CSCALE)
        fig2.update_traces(texttemplate='%{text:.2s}', textposition='outside',
                           textfont=dict(size=9,color='#5a5a7a'), marker_line_width=0)
        tfig(fig2, 'RANKED RUN SCORERS')
        fig2.update_layout(coloraxis_showscale=False, yaxis=dict(tickfont=dict(size=9)))
        st.plotly_chart(fig2, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
#  BOWLER
# ══════════════════════════════════════════════════════════════════════════════
elif user_menu == '◎  Bowler':
    page_header('Bowling Records', 'Top', 'Bowlers')

    bowler_list = helper.Bolwer_Run(Deliveries)
    Selected_bowler = st.selectbox('Select Bowler', bowler_list)
    Bowler_df = helper.fetch_Bowler_Run(Deliveries, Selected_bowler)
    st.dataframe(Bowler_df, use_container_width=True, hide_index=True)

    Ball   = Deliveries.groupby("bowler")['total_runs'].sum().sort_values(ascending=False)
    Top25b = Ball.head(25).reset_index()
    Top25b.columns = ['Bowler','Total Runs']
    tbow   = Top25b.iloc[0]

    st.markdown(f"""
    <div class="kpi-grid">
      {kpi('🎯', tbow['Total Runs'], 'Most Conceded · '+tbow['Bowler'])}
      {kpi('📊', len(bowler_list)-1, 'Total Bowlers')}
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap='large')
    with col1:
        section_label('Line Chart')
        fig = px.line(Top25b, x='Bowler', y='Total Runs', markers=True)
        fig.update_traces(
            line=dict(color='#ff3366', width=2.5),
            marker=dict(color='#ff8800', size=8, line=dict(color='#ff3366', width=1.5)),
            fill='tozeroy', fillcolor='rgba(255,51,102,0.05)'
        )
        tfig(fig, 'RUNS CONCEDED — TOP 25')
        fig.update_xaxes(tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section_label('Share — Donut')
        fig2 = go.Figure(go.Pie(
            labels=Top25b['Bowler'], values=Top25b['Total Runs'],
            hole=0.5, textinfo='percent',
            textfont=dict(family='Outfit', size=10, color='#f0f0f8'),
            marker=dict(
                colors=['#ff8800','#ffd700','#ff3366','#00d4ff','#a855f7','#22c55e']*5,
                line=dict(color='#04040a', width=2)
            )
        ))
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Outfit', color='#5a5a7a'),
            height=500
        )
        fig2.update_layout(title=dict(text='RUNS SHARE'))
        st.plotly_chart(fig2, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
#  BOUNDARIES
# ══════════════════════════════════════════════════════════════════════════════
elif user_menu == '◆  Boundaries':
    page_header('Shot Analysis', 'Boundary', 'Stats')

    Runs_list, Batsmans_list = helper.boundry(Deliveries)
    col1, col2 = st.columns(2, gap='medium')
    with col1: Selected_Runs     = st.selectbox('Run Type', Runs_list)
    with col2: Selected_Batsmans = st.selectbox('Batsman',  Batsmans_list)

    Bdf = helper.count_boundaries(Deliveries, Selected_Runs, Selected_Batsmans)
    st.dataframe(Bdf, use_container_width=True, hide_index=True)
    st.markdown('<div class="strip"></div>', unsafe_allow_html=True)

    M4 = Deliveries['batsman_runs'] == 4
    M6 = Deliveries['batsman_runs'] == 6
    PHF = Deliveries[M4].groupby('batsman')['batsman_runs'].count().reset_index()
    PHF.columns = ['Batsman','Fours']
    PHF = PHF.sort_values('Fours', ascending=False).head(25)
    PHS = Deliveries[M6].groupby('batsman')['batsman_runs'].count().reset_index()
    PHS.columns = ['Batsman','Sixes']
    PHS = PHS.sort_values('Sixes', ascending=False).head(25)

    tf = PHF.iloc[0]; ts = PHS.iloc[0]
    st.markdown(f"""
    <div class="kpi-grid">
      {kpi('4️⃣', tf['Fours'], 'Most Fours · '+tf['Batsman'])}
      {kpi('6️⃣', ts['Sixes'], 'Most Sixes · '+ts['Batsman'])}
      {kpi('💥', int(PHF['Fours'].sum()+PHS['Sixes'].sum()), 'Total Boundaries')}
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap='large')
    with col1:
        section_label('Fours Distribution')
        af = Deliveries[M4].groupby('batsman')['batsman_runs'].count().reset_index()
        af.columns = ['Batsman','Fours']
        fig = px.histogram(af, x='Fours', nbins=25, color_discrete_sequence=['#ff8800'])
        fig.update_traces(marker_line_width=0, opacity=0.85)
        tfig(fig, 'FOURS DISTRIBUTION')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section_label('Top Sixes Hitters')
        fig2 = px.area(PHS, x='Batsman', y='Sixes', markers=True,
                       color_discrete_sequence=['#ffd700'])
        fig2.update_traces(
            fillcolor='rgba(255,215,0,0.07)',
            line=dict(width=2.5),
            marker=dict(size=7, color='#ffd700', line=dict(color='#ff8800', width=1.5))
        )
        tfig(fig2, 'SIXES — TOP 25')
        fig2.update_xaxes(tickangle=-45)
        st.plotly_chart(fig2, use_container_width=True)

    section_label('Fours vs Sixes — Combined')
    PS = PHF.merge(PHS, on='Batsman', how='outer').fillna(0).sort_values('Fours', ascending=False)
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=PS['Batsman'], y=PS['Fours'], name='Fours', mode='lines+markers',
        line=dict(color='#ff8800', width=2.5),
        marker=dict(size=7, color='#ff8800', line=dict(color='#ffd700', width=1.5)),
        fill='tozeroy', fillcolor='rgba(255,136,0,0.05)'
    ))
    fig3.add_trace(go.Scatter(
        x=PS['Batsman'], y=PS['Sixes'], name='Sixes', mode='lines+markers',
        line=dict(color='#ffd700', width=2.5, dash='dot'),
        marker=dict(size=7, color='#ffd700', line=dict(color='#ff8800', width=1.5)),
        fill='tozeroy', fillcolor='rgba(255,215,0,0.04)'
    ))
    fig3.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        height=500
    )
    fig3.update_layout(title=dict(text='FOURS VS SIXES'))
    st.plotly_chart(fig3, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
#  BATSMAN SCORE
# ══════════════════════════════════════════════════════════════════════════════
elif user_menu == '▣  Batsman Score':
    page_header('Match Breakdown', 'Batsman', 'Score')

    BL2 = helper.batsman(Deliveries)
    sel = st.selectbox('Select Batsman', BL2)
    bd  = Deliveries[Deliveries['batsman'] == sel]
    rbt = (bd.groupby('bowling_team')['batsman_runs']
             .sum().reset_index(name='Runs')
             .sort_values('Runs', ascending=False))

    if not rbt.empty:
        bv = rbt.iloc[0]
        st.markdown(f"""
        <div class="kpi-grid">
          {kpi('🏏', int(rbt['Runs'].sum()), 'Career Runs')}
          {kpi('⚔️', bv['Runs'],            'Best vs · '+bv['bowling_team'])}
          {kpi('🆚', len(rbt),              'Teams Faced')}
        </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2], gap='large')
    with col1:
        section_label('Runs vs Teams')
        st.dataframe(rbt, use_container_width=True, hide_index=True)
    with col2:
        section_label('Chart')
        bp = helper.batsman_scored(Deliveries, sel)
        if bp is not None:
            bp.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                height=500
            )
            st.plotly_chart(bp, use_container_width=True)
        else:
            st.info(f'No data for {sel}.')

# ══════════════════════════════════════════════════════════════════════════════
#  ORANGE CAP
# ══════════════════════════════════════════════════════════════════════════════
elif user_menu == '●  Orange Cap':
    page_header('Season Leaders', 'Orange', 'Cap')

    SL2  = helper.season(Matches)
    SS2  = st.selectbox('Select Season', SL2)
    OCT  = helper.orange_cap_holder(Deliveries, Matches, SS2)
    st.dataframe(OCT, use_container_width=True, hide_index=True)
    st.markdown('<div class="strip"></div>', unsafe_allow_html=True)

    Merge = Deliveries.merge(Matches, left_on='match_id', right_on='id')
    OC    = Merge.groupby(['season','batsman'])['batsman_runs'].sum().sort_values(ascending=False).reset_index()
    OCH   = OC.drop_duplicates(subset='season', keep='first').sort_values('season').reset_index(drop=True)
    OCH.columns = ['Season','Batsman','Runs']

    col1, col2 = st.columns(2, gap='large')
    with col1:
        section_label('Runs per Season')
        fig = px.bar(OCH, x='Season', y='Runs', text='Batsman',
                     color='Runs', color_continuous_scale=CSCALE)
        fig.update_traces(textposition='outside',
                          textfont=dict(size=9,color='#5a5a7a'), marker_line_width=0)
        tfig(fig, 'ORANGE CAP RUNS')
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section_label('Scatter Timeline')
        OCH['enc'] = OCH['Batsman'].factorize()[0]
        fig2 = px.scatter(OCH, x='Season', y='enc', text='Batsman',
                          size='Runs', color='Runs', color_continuous_scale=CSCALE,
                          hover_data={'Batsman':True,'Runs':True,'enc':False})
        fig2.update_traces(
            textposition='top center',
            textfont=dict(size=9, color='#5a5a7a', family='Outfit'),
            marker=dict(line=dict(color='rgba(255,136,0,0.4)', width=1))
        )
        tfig(fig2, 'CAP HOLDERS TIMELINE')
        fig2.update_layout(
            coloraxis_showscale=False,
            yaxis=dict(
                tickvals=list(range(OCH['Batsman'].nunique())),
                ticktext=OCH['Batsman'].unique(),
                tickfont=dict(size=9),
                gridcolor='rgba(255,255,255,0.04)'
            )
        )
        st.plotly_chart(fig2, use_container_width=True)

    section_label('Radial — Runs by Season')
    fig3 = go.Figure(go.Barpolar(
        r=OCH['Runs'], theta=OCH['Season'].astype(str), width=0.8,
        marker=dict(
            color=OCH['Runs'],
            colorscale=[[0,'#1a0a00'],[0.5,'#ff8800'],[1,'#ffd700']],
            line=dict(color='rgba(255,136,0,0.2)', width=1)
        )
    ))
    fig3.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Outfit', color='#5a5a7a'),
        height=550,
        title=dict(text='RADIAL RUN VIEW'),
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(gridcolor='rgba(255,255,255,0.04)',
                            linecolor='rgba(255,255,255,0.06)',
                            tickfont=dict(size=9,color='#5a5a7a')),
            angularaxis=dict(gridcolor='rgba(255,255,255,0.04)',
                             linecolor='rgba(255,255,255,0.06)',
                             tickfont=dict(size=10,color='#5a5a7a'))
        )
    )
    st.plotly_chart(fig3, use_container_width=True)
