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
# Mobile-first styling
# ---------------------------

st.markdown("""
<style>
.block-container {
    padding-top: 0.7rem;
    padding-left: 0.75rem;
    padding-right: 0.75rem;
    max-width: 1050px;
}
.oasl-hero {
    background: linear-gradient(135deg, #06131f 0%, #064e3b 55%, #0f766e 100%);
    color: white;
    padding: 20px;
    border-radius: 22px;
    margin-bottom: 16px;
    box-shadow: 0 8px 28px rgba(0,0,0,.22);
}
.oasl-card {
    padding: 15px;
    border-radius: 18px;
    border: 1px solid rgba(148,163,184,.25);
    background: rgba(15,23,42,.055);
    margin-bottom: 12px;
}
.oasl-dark-card {
    padding: 15px;
    border-radius: 18px;
    background: #0f172a;
    color: white;
    margin-bottom: 12px;
}
.oasl-pill {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 999px;
    background: #dcfce7;
    color: #166534;
    font-weight: 700;
    font-size: 13px;
}
.oasl-warning {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 999px;
    background: #fef3c7;
    color: #92400e;
    font-weight: 700;
    font-size: 13px;
}
button {
    border-radius: 14px !important;
    min-height: 44px !important;
}
div[data-testid="stMetric"] {
    background: rgba(15,23,42,.045);
    padding: 12px;
    border-radius: 16px;
    border: 1px solid rgba(148,163,184,.20);
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Demo AI data and functions
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
    {"match": "Panthers vs Rabbitohs", "home": "Panthers", "away": "Rabbitohs", "venue": "BlueBet Stadium", "weather": "Dry"},
    {"match": "Storm vs Broncos", "home": "Storm", "away": "Broncos", "venue": "AAMI Park", "weather": "Light rain"},
    {"match": "Cowboys vs Dolphins", "home": "Cowboys", "away": "Dolphins", "venue": "Queensland Country Bank Stadium", "weather": "Humid"},
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
    return p_home, home_rating, away_rating

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
    rating = (
        row["form"] * .32
        + row["opponent"] * .24
        + row["venue"] * .13
        + row["weather"] * .10
        + channel_bonus * .21
    )
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
        p_home, h_rating, a_rating = win_probability(m["home"], m["away"])
        winner = m["home"] if p_home >= .5 else m["away"]
        prob = p_home if winner == m["home"] else 1 - p_home
        hs, as_ = expected_score(m["home"], m["away"])
        rows.append({
            "Match": m["match"],
            "Venue": m["venue"],
            "Weather": m["weather"],
            "Predicted Winner": winner,
            "Win %": round(prob * 100, 1),
            "Expected Score": f"{m['home']} {hs} - {m['away']} {as_}",
            "Confidence": "High" if prob >= .72 else ("Medium" if prob >= .60 else "Low"),
            "Why": f"{winner} has the stronger combined attack, defence and momentum profile.",
        })
    return pd.DataFrame(rows)

def confidence_colour(label):
    return "🟢" if label == "High" else ("🟡" if label == "Medium" else "🔴")

# ---------------------------
# App state
# ---------------------------

if "engine_ran" not in st.session_state:
    st.session_state.engine_ran = False

# ---------------------------
# Header
# ---------------------------

st.markdown("""
<div class="oasl-hero">
<h1 style="margin:0;font-size:32px;">🏉 Oggy's AI Sports Lab</h1>
<p style="margin:8px 0 0 0;font-size:16px;opacity:.9;">AI-powered NRL prediction command centre</p>
</div>
""", unsafe_allow_html=True)

left, right = st.columns(2)
with left:
    if st.button("🚀 Load Demo Data", use_container_width=True):
        st.success("Demo data loaded.")
with right:
    if st.button("🧠 Run AI Engine", use_container_width=True):
        st.session_state.engine_ran = True
        st.success("AI engine complete.")

if not st.session_state.engine_ran:
    st.info("Tap **Run AI Engine** to view the production demo.")
    st.stop()

matches = match_predictions()
tries = try_markets()

# ---------------------------
# Home dashboard
# ---------------------------

st.markdown("## 🏠 Command Centre")

best_match = matches.iloc[0]
best_try = tries.iloc[0]

c1, c2, c3 = st.columns(3)
c1.metric("Best Winner", best_match["Predicted Winner"], f"{best_match['Win %']}%")
c2.metric("Top Try Pick", best_try["player"], f"{best_try['Anytime %']}%")
c3.metric("AI Confidence", best_match["Confidence"], confidence_colour(best_match["Confidence"]))

st.markdown("## 🏆 Match Winner AI")

for _, row in matches.iterrows():
    st.markdown(f"""
    <div class="oasl-card">
        <span class="oasl-pill">{row['Confidence']} Confidence</span>
        <h3 style="margin-bottom:4px;">{row['Match']}</h3>
        <p><b>Venue:</b> {row['Venue']} &nbsp; | &nbsp; <b>Weather:</b> {row['Weather']}</p>
        <h2 style="margin:4px 0;">{row['Predicted Winner']} — {row['Win %']}%</h2>
        <p><b>Expected Score:</b> {row['Expected Score']}</p>
        <p><b>Why:</b> {row['Why']}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("## 🎯 Try Scorer Centre")

show_cols = ["player", "team", "position", "last5", "Anytime %", "First Try %", "2+ %", "3+ %", "Fair Odds", "AI Rating"]
st.dataframe(tries[show_cols], use_container_width=True, hide_index=True)

st.markdown("## 🤖 Why AI Likes The Top Pick")

st.markdown(f"""
<div class="oasl-dark-card">
    <h2 style="margin-top:0;">🔥 {best_try['player']}</h2>
    <p><b>Team:</b> {best_try['team']} &nbsp; | &nbsp; <b>Position:</b> {best_try['position']}</p>
    <p><b>Last 5:</b> {best_try['last5']}</p>
    <p><b>Anytime Try:</b> {best_try['Anytime %']}% &nbsp; | &nbsp; <b>Fair Odds:</b> {best_try['Fair Odds']}</p>
    <p><b>AI Rating:</b> {best_try['AI Rating']}</p>
    <hr>
    <p>AI likes this pick because of strong recent form, high team attack rating, a strong scoring channel, and a favourable opponent profile.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("## 🧬 Team DNA Snapshot")

team_view = TEAMS.copy()
team_view["Overall DNA"] = (
    team_view["attack"] * .32 + team_view["defence"] * .30 + team_view["momentum"] * .23 + team_view[["right_edge", "middle", "left_edge"]].max(axis=1) * .15
).round(1)
st.dataframe(team_view.sort_values("Overall DNA", ascending=False), use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("Oggy's AI Sports Lab Production V1 — demo app. Replace demo data with real NRL data as the next stage.")
