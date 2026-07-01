import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Oggy's AI Sports Lab",
    page_icon="🏉",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------
# Compact mobile-first styling
# ---------------------------

st.markdown("""
<style>
html, body, [class*="css"] {
    font-size: 14px !important;
}
.block-container {
    padding-top: 0.45rem;
    padding-left: 0.65rem;
    padding-right: 0.65rem;
    max-width: 1050px;
}
h1 {
    font-size: 26px !important;
    line-height: 1.15 !important;
}
h2 {
    font-size: 20px !important;
    margin-top: 0.55rem !important;
    margin-bottom: 0.4rem !important;
}
h3 {
    font-size: 17px !important;
    margin-top: 0.25rem !important;
    margin-bottom: 0.2rem !important;
}
p, li, div {
    font-size: 14px;
}
.oasl-hero {
    background: linear-gradient(135deg, #06131f 0%, #064e3b 55%, #0f766e 100%);
    color: white;
    padding: 14px 15px;
    border-radius: 18px;
    margin-bottom: 10px;
    box-shadow: 0 6px 20px rgba(0,0,0,.18);
}
.oasl-card {
    padding: 11px 12px;
    border-radius: 15px;
    border: 1px solid rgba(148,163,184,.25);
    background: rgba(15,23,42,.045);
    margin-bottom: 8px;
}
.oasl-dark-card {
    padding: 12px;
    border-radius: 16px;
    background: #0f172a;
    color: white;
    margin-bottom: 9px;
}
.oasl-pill {
    display: inline-block;
    padding: 3px 8px;
    border-radius: 999px;
    background: #dcfce7;
    color: #166534;
    font-weight: 700;
    font-size: 12px;
}
.oasl-warning {
    display: inline-block;
    padding: 3px 8px;
    border-radius: 999px;
    background: #fef3c7;
    color: #92400e;
    font-weight: 700;
    font-size: 12px;
}
button {
    border-radius: 12px !important;
    min-height: 38px !important;
    font-size: 14px !important;
}
div[data-testid="stMetric"] {
    background: rgba(15,23,42,.045);
    padding: 8px 9px;
    border-radius: 13px;
    border: 1px solid rgba(148,163,184,.20);
}
div[data-testid="stMetric"] label {
    font-size: 12px !important;
}
div[data-testid="stMetric"] div {
    font-size: 15px !important;
}
[data-testid="stDataFrame"] {
    font-size: 12px !important;
}
.small-muted {
    font-size: 12px;
    opacity: .75;
}
.quick-row {
    display:flex;
    justify-content:space-between;
    gap:8px;
    align-items:center;
}
.score-big {
    font-size: 18px;
    font-weight: 800;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Demo data and calculations
# ---------------------------

TEAMS = pd.DataFrame([
    {"team": "Panthers", "attack": 96, "defence": 94, "momentum": 93, "right_edge": 98, "middle": 88, "left_edge": 91},
    {"team": "Rabbitohs", "attack": 74, "defence": 68, "momentum": 62, "right_edge": 73, "middle": 71, "left_edge": 66},
    {"team": "Storm", "attack": 91, "defence": 89, "momentum": 88, "right_edge": 90, "middle": 92, "left_edge": 86},
    {"team": "Broncos", "attack": 87, "defence": 82, "momentum": 84, "right_edge": 86, "middle": 83, "left_edge": 88},
    {"team": "Cowboys", "attack": 81, "defence": 76, "momentum": 78, "right_edge": 82, "middle": 77, "left_edge": 80},
    {"team": "Dolphins", "attack": 79, "defence": 75, "momentum": 76, "right_edge": 78, "middle": 82, "left_edge": 74},
])

MATCHES = pd.DataFrame([
    {"match": "Panthers vs Rabbitohs", "home": "Panthers", "away": "Rabbitohs", "venue": "BlueBet", "weather": "Dry"},
    {"match": "Storm vs Broncos", "home": "Storm", "away": "Broncos", "venue": "AAMI Park", "weather": "Light rain"},
    {"match": "Cowboys vs Dolphins", "home": "Cowboys", "away": "Dolphins", "venue": "QCB Stadium", "weather": "Humid"},
])

PLAYERS = pd.DataFrame([
    {"player": "Thomas Jenkins", "team": "Panthers", "position": "Centre", "last5": "2️⃣0️⃣2️⃣0️⃣2️⃣", "form": 97, "opponent": 95, "venue": 91, "weather": 90, "channel": "Right Edge"},
    {"player": "Brian To'o", "team": "Panthers", "position": "Winger", "last5": "1️⃣1️⃣2️⃣1️⃣1️⃣", "form": 94, "opponent": 91, "venue": 92, "weather": 88, "channel": "Left Edge"},
    {"player": "Isaah Yeo", "team": "Panthers", "position": "Lock", "last5": "0️⃣1️⃣0️⃣0️⃣1️⃣", "form": 78, "opponent": 82, "venue": 86, "weather": 84, "channel": "Middle"},
    {"player": "Storm Winger", "team": "Storm", "position": "Winger", "last5": "1️⃣1️⃣1️⃣2️⃣1️⃣", "form": 92, "opponent": 87, "venue": 89, "weather": 80, "channel": "Right Edge"},
    {"player": "Broncos Winger", "team": "Broncos", "position": "Winger", "last5": "1️⃣0️⃣2️⃣1️⃣0️⃣", "form": 84, "opponent": 81, "venue": 80, "weather": 82, "channel": "Left Edge"},
    {"player": "Rabbitohs Fullback", "team": "Rabbitohs", "position": "Fullback", "last5": "1️⃣0️⃣1️⃣0️⃣0️⃣", "form": 73, "opponent": 66, "venue": 75, "weather": 78, "channel": "Kick / Other"},
    {"player": "Cowboys Centre", "team": "Cowboys", "position": "Centre", "last5": "1️⃣0️⃣1️⃣1️⃣0️⃣", "form": 82, "opponent": 79, "venue": 84, "weather": 81, "channel": "Right Edge"},
    {"player": "Dolphins Forward", "team": "Dolphins", "position": "Prop", "last5": "0️⃣0️⃣1️⃣0️⃣1️⃣", "form": 76, "opponent": 78, "venue": 76, "weather": 79, "channel": "Middle"},
])

def team_row(team):
    return TEAMS[TEAMS["team"] == team].iloc[0]

def win_probability(home, away):
    h = team_row(home)
    a = team_row(away)
    home_rating = h["attack"] * .32 + h["defence"] * .30 + h["momentum"] * .24 + 3
    away_rating = a["attack"] * .32 + a["defence"] * .30 + a["momentum"] * .24
    diff = home_rating - away_rating
    p_home = 1 / (1 + np.exp(-diff / 10.5))
    return p_home

def expected_score(home, away):
    h = team_row(home)
    a = team_row(away)
    home_score = 14 + h["attack"] * .23 - a["defence"] * .09 + 3
    away_score = 14 + a["attack"] * .23 - h["defence"] * .09
    return max(round(home_score), 6), max(round(away_score), 6)

def player_rating(row):
    team = team_row(row["team"])
    channel_bonus = {
        "Right Edge": team["right_edge"],
        "Left Edge": team["left_edge"],
        "Middle": team["middle"],
        "Kick / Other": team["attack"],
    }.get(row["channel"], team["attack"])
    rating = row["form"]*.32 + row["opponent"]*.24 + row["venue"]*.13 + row["weather"]*.10 + channel_bonus*.21
    return round(rating, 1)

def try_markets():
    df = PLAYERS.copy()
    df["AI Rating"] = df.apply(player_rating, axis=1)
    df["Anytime %"] = (df["AI Rating"] / 128).clip(.05, .82)
    df["First Try %"] = (df["Anytime %"] * .25).clip(.01, .28)
    df["2+ %"] = (df["Anytime %"] * .42).clip(.01, .40)
    df["3+ %"] = (df["Anytime %"] * .13).clip(.005, .16)
    df["Fair Odds"] = (1 / df["Anytime %"]).round(2)
    for c in ["Anytime %", "First Try %", "2+ %", "3+ %"]:
        df[c] = (df[c] * 100).round(1)
    return df.sort_values("AI Rating", ascending=False)

def match_predictions():
    rows = []
    for _, m in MATCHES.iterrows():
        p_home = win_probability(m["home"], m["away"])
        winner = m["home"] if p_home >= .5 else m["away"]
        prob = p_home if winner == m["home"] else 1 - p_home
        hs, as_ = expected_score(m["home"], m["away"])
        rows.append({
            "Match": m["match"],
            "Venue": m["venue"],
            "Weather": m["weather"],
            "Winner": winner,
            "Win %": round(prob * 100, 1),
            "Score": f"{m['home']} {hs} - {m['away']} {as_}",
            "Confidence": "High" if prob >= .72 else ("Medium" if prob >= .60 else "Low"),
            "Why": f"{winner} has the stronger attack/defence/momentum profile.",
        })
    return pd.DataFrame(rows)

def confidence_colour(label):
    return "🟢" if label == "High" else ("🟡" if label == "Medium" else "🔴")

# ---------------------------
# App
# ---------------------------

if "engine_ran" not in st.session_state:
    st.session_state.engine_ran = False

st.markdown("""
<div class="oasl-hero">
<h1 style="margin:0;">🏉 Oggy's AI Sports Lab</h1>
<p style="margin:6px 0 0 0;font-size:13px;opacity:.9;">AI-powered NRL prediction command centre</p>
</div>
""", unsafe_allow_html=True)

left, right = st.columns(2)
with left:
    if st.button("🚀 Load Data", use_container_width=True):
        st.success("Demo data loaded.")
with right:
    if st.button("🧠 Run AI", use_container_width=True):
        st.session_state.engine_ran = True
        st.success("AI engine complete.")

if not st.session_state.engine_ran:
    st.info("Tap **Run AI** to view the compact v1.1 demo.")
    st.stop()

matches = match_predictions()
tries = try_markets()
best_match = matches.iloc[0]
best_try = tries.iloc[0]

st.markdown("## 🏠 Dashboard")

c1, c2, c3 = st.columns(3)
c1.metric("Best Winner", best_match["Winner"], f"{best_match['Win %']}%")
c2.metric("Top Try", best_try["player"], f"{best_try['Anytime %']}%")
c3.metric("Confidence", best_match["Confidence"], confidence_colour(best_match["Confidence"]))

st.markdown(f"""
<div class="oasl-dark-card">
    <div class="quick-row">
        <div>
            <span class="oasl-pill">AI Pick</span>
            <h3>🔥 {best_try['player']}</h3>
            <p class="small-muted">{best_try['team']} • {best_try['position']} • Last 5 {best_try['last5']}</p>
        </div>
        <div class="score-big">{best_try['Anytime %']}%</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("## 🏆 Match Winner AI")

for _, row in matches.iterrows():
    st.markdown(f"""
    <div class="oasl-card">
        <div class="quick-row">
            <div>
                <span class="oasl-pill">{row['Confidence']}</span>
                <h3>{row['Match']}</h3>
                <p class="small-muted">{row['Venue']} • {row['Weather']}</p>
            </div>
            <div class="score-big">{row['Win %']}%</div>
        </div>
        <p><b>{row['Winner']}</b> • {row['Score']}</p>
        <p class="small-muted">{row['Why']}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("## 🎯 Try Scorer Centre")

show_cols = ["player", "team", "position", "last5", "Anytime %", "First Try %", "2+ %", "3+ %", "Fair Odds", "AI Rating"]
st.dataframe(tries[show_cols], use_container_width=True, hide_index=True)

st.markdown("## 🤖 Why Top Pick?")

st.markdown(f"""
<div class="oasl-card">
    <h3>🔥 {best_try['player']}</h3>
    <p><b>Anytime:</b> {best_try['Anytime %']}% • <b>Fair:</b> {best_try['Fair Odds']}</p>
    <p><b>Last 5:</b> {best_try['last5']}</p>
    <p class="small-muted">Strong recent form, strong team attack, favourable opponent profile, and strong scoring channel.</p>
</div>
""", unsafe_allow_html=True)

with st.expander("🧬 Team DNA Snapshot"):
    team_view = TEAMS.copy()
    team_view["Overall DNA"] = (
        team_view["attack"]*.32 + team_view["defence"]*.30 + team_view["momentum"]*.23 + team_view[["right_edge", "middle", "left_edge"]].max(axis=1)*.15
    ).round(1)
    st.dataframe(team_view.sort_values("Overall DNA", ascending=False), use_container_width=True, hide_index=True)

st.caption("Oggy's AI Sports Lab v1.1 Compact Mobile UI")
