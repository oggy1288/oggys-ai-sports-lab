import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Oggy's AI Sports Lab", page_icon="🏉", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
html, body, [class*="css"] {font-size:13px !important;}
.block-container {padding-top:.35rem; padding-left:.6rem; padding-right:.6rem; max-width:1050px;}
h1 {font-size:24px !important; line-height:1.12 !important;}
h2 {font-size:18px !important; margin:.45rem 0 .35rem 0 !important;}
h3 {font-size:16px !important; margin:.18rem 0 .12rem 0 !important;}
p, li, div {font-size:13px;}
.oasl-hero {background:linear-gradient(135deg,#06131f,#064e3b,#0f766e); color:white; padding:12px 13px; border-radius:17px; margin-bottom:9px;}
.oasl-card {padding:10px 11px; border-radius:15px; border:1px solid rgba(148,163,184,.25); background:rgba(15,23,42,.045); margin-bottom:8px;}
.pill-green {display:inline-block;padding:3px 8px;border-radius:999px;background:#dcfce7;color:#166534;font-weight:700;font-size:11px;}
.pill-yellow {display:inline-block;padding:3px 8px;border-radius:999px;background:#fef3c7;color:#92400e;font-weight:700;font-size:11px;}
.pill-orange {display:inline-block;padding:3px 8px;border-radius:999px;background:#ffedd5;color:#9a3412;font-weight:700;font-size:11px;}
.pill-red {display:inline-block;padding:3px 8px;border-radius:999px;background:#fee2e2;color:#991b1b;font-weight:700;font-size:11px;}
.quick-row {display:flex;justify-content:space-between;gap:8px;align-items:center;}
.big-num {font-size:18px;font-weight:900;}
.muted {font-size:12px;opacity:.72;}
.navbar {position:sticky; bottom:0; background:rgba(15,23,42,.96); color:white; padding:8px; border-radius:16px; margin-top:10px; display:flex; justify-content:space-around;}
.navitem {font-size:11px;text-align:center;}
button {border-radius:12px !important; min-height:36px !important; font-size:13px !important;}
</style>
""", unsafe_allow_html=True)

DEFAULT_PLAYERS = pd.DataFrame([
    {"Player":"Thomas Jenkins","Team":"Panthers","Position":"Centre","Last5":"2-0-2-0-2","Form":97,"Opponent":95,"TeamAttack":96,"WeatherFit":90,"BookOdds":1.90},
    {"Player":"Brian To'o","Team":"Panthers","Position":"Winger","Last5":"1-1-2-1-1","Form":94,"Opponent":91,"TeamAttack":96,"WeatherFit":88,"BookOdds":1.75},
    {"Player":"Isaah Yeo","Team":"Panthers","Position":"Lock","Last5":"0-1-0-0-1","Form":78,"Opponent":82,"TeamAttack":96,"WeatherFit":84,"BookOdds":5.50},
    {"Player":"Storm Winger","Team":"Storm","Position":"Winger","Last5":"1-1-1-2-1","Form":92,"Opponent":87,"TeamAttack":91,"WeatherFit":80,"BookOdds":2.10},
    {"Player":"Broncos Winger","Team":"Broncos","Position":"Winger","Last5":"1-0-2-1-0","Form":84,"Opponent":81,"TeamAttack":87,"WeatherFit":82,"BookOdds":2.45},
])

DEFAULT_GAMES = pd.DataFrame([
    {"Game":"Panthers vs Rabbitohs","Home":"Panthers","Away":"Rabbitohs","HomeRating":94,"AwayRating":72,"Weather":"Dry"},
    {"Game":"Storm vs Broncos","Home":"Storm","Away":"Broncos","HomeRating":89,"AwayRating":84,"Weather":"Light rain"},
    {"Game":"Cowboys vs Dolphins","Home":"Cowboys","Away":"Dolphins","HomeRating":81,"AwayRating":77,"Weather":"Humid"},
])

def pct_pill(v):
    if v >= 80: return "pill-green"
    if v >= 60: return "pill-yellow"
    if v >= 45: return "pill-orange"
    return "pill-red"

def visual_last5(seq):
    out = []
    for x in str(seq).replace(",", "-").split("-"):
        x = x.strip()
        if x == "0": out.append("0️⃣")
        elif x == "1": out.append("1️⃣")
        elif x == "2": out.append("2️⃣")
        elif x == "3": out.append("3️⃣")
        else: out.append(x)
    return "".join(out)

def calc_player_predictions(df):
    rows = []
    for _, r in df.iterrows():
        form = float(r.get("Form", 70))
        opp = float(r.get("Opponent", 70))
        attack = float(r.get("TeamAttack", 70))
        weather = float(r.get("WeatherFit", 80))
        odds = float(r.get("BookOdds", 0) or 0)
        rating = form*.35 + opp*.25 + attack*.25 + weather*.15
        anytime = min(.85, max(.04, rating/128))
        first = min(.30, anytime*.25)
        two = min(.42, anytime*.42)
        three = min(.18, anytime*.13)
        fair = 1 / anytime
        edge = ((odds / fair) - 1) * 100 if odds > 0 else 0
        rec = "BET" if edge >= 12 and anytime >= .45 else ("WATCH" if edge >= 3 else "NO VALUE")
        rows.append({
            "Player": r.get("Player",""),
            "Team": r.get("Team",""),
            "Position": r.get("Position",""),
            "Last 5": visual_last5(r.get("Last5","")),
            "AI Rating": round(rating,1),
            "Anytime %": round(anytime*100,1),
            "First Try %": round(first*100,1),
            "2+ %": round(two*100,1),
            "3+ %": round(three*100,1),
            "Fair Odds": round(fair,2),
            "Book Odds": odds,
            "Edge %": round(edge,1),
            "Recommendation": rec,
        })
    return pd.DataFrame(rows).sort_values(["Recommendation","Edge %","Anytime %"], ascending=[True,False,False])

def calc_game_predictions(df):
    rows = []
    for _, r in df.iterrows():
        home_rating = float(r.get("HomeRating", 75))
        away_rating = float(r.get("AwayRating", 75))
        diff = home_rating - away_rating + 3
        p_home = 1 / (1 + np.exp(-diff/11))
        winner = r.get("Home") if p_home >= .5 else r.get("Away")
        prob = p_home if winner == r.get("Home") else 1-p_home
        hs = max(round(16 + home_rating*.18 - away_rating*.06 + 2), 6)
        aw = max(round(16 + away_rating*.18 - home_rating*.06), 6)
        rows.append({
            "Game": r.get("Game",""),
            "Winner": winner,
            "Win %": round(prob*100,1),
            "Expected Score": f"{r.get('Home')} {hs} - {r.get('Away')} {aw}",
            "Weather": r.get("Weather",""),
            "Confidence": "High" if prob >= .70 else ("Medium" if prob >= .58 else "Low"),
        })
    return pd.DataFrame(rows).sort_values("Win %", ascending=False)

if "players_input" not in st.session_state:
    st.session_state.players_input = DEFAULT_PLAYERS.copy()
if "games_input" not in st.session_state:
    st.session_state.games_input = DEFAULT_GAMES.copy()
if "ran" not in st.session_state:
    st.session_state.ran = False

st.markdown("""
<div class="oasl-hero">
<h1 style="margin:0;">🏉 Oggy's AI Sports Lab</h1>
<p style="margin:5px 0 0 0;font-size:12px;opacity:.9;">v1.3 Manual Live Round Mode</p>
</div>
""", unsafe_allow_html=True)

tab_home, tab_live, tab_results = st.tabs(["🏠 Home", "✍️ Enter Live Data", "📊 Predictions"])

with tab_home:
    st.markdown("## Today Mode")
    st.write("Enter this week’s games, players and odds manually. The app will rank winner picks, try scorer picks, fair odds and value.")
    if st.button("🧠 Run AI On Current Data", use_container_width=True):
        st.session_state.ran = True
        st.success("AI updated.")

with tab_live:
    st.markdown("## 🏉 Games")
    st.session_state.games_input = st.data_editor(
        st.session_state.games_input,
        num_rows="dynamic",
        use_container_width=True,
        key="games_editor",
    )
    st.markdown("## 🎯 Players / Odds")
    st.session_state.players_input = st.data_editor(
        st.session_state.players_input,
        num_rows="dynamic",
        use_container_width=True,
        key="players_editor",
    )
    if st.button("✅ Save & Run AI", use_container_width=True):
        st.session_state.ran = True
        st.success("Saved and ranked.")

with tab_results:
    if not st.session_state.ran:
        st.info("Go to Home or Enter Live Data, then tap **Run AI**.")
    else:
        games = calc_game_predictions(st.session_state.games_input)
        players = calc_player_predictions(st.session_state.players_input)

        st.markdown("## 🏠 Dashboard")
        top_game = games.iloc[0]
        top_try = players.iloc[0]
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""<div class="oasl-card"><span class="{pct_pill(top_game['Win %'])}">🏆 Best Winner</span><h3>{top_game['Winner']}</h3><div class="big-num">{top_game['Win %']}%</div><p class="muted">{top_game['Game']}</p></div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class="oasl-card"><span class="{pct_pill(top_try['Anytime %'])}">🔥 Best Try</span><h3>{top_try['Player']}</h3><div class="big-num">{top_try['Anytime %']}%</div><p class="muted">{top_try['Last 5']} • {top_try['Recommendation']}</p></div>""", unsafe_allow_html=True)

        st.markdown("## 🏉 Match Cards")
        for _, r in games.iterrows():
            st.markdown(f"""
            <div class="oasl-card">
                <div class="quick-row">
                    <div><span class="{pct_pill(r['Win %'])}">{r['Confidence']}</span><h3>{r['Game']}</h3><p class="muted">{r['Weather']}</p></div>
                    <div class="big-num">{r['Win %']}%</div>
                </div>
                <p><b>{r['Winner']}</b> • {r['Expected Score']}</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("## 🎯 Try Scorer Cards")
        for _, r in players.head(10).iterrows():
            st.markdown(f"""
            <div class="oasl-card">
                <div class="quick-row">
                    <div><span class="{pct_pill(r['Anytime %'])}">{r['Recommendation']}</span><h3>{r['Player']}</h3><p class="muted">{r['Team']} • {r['Position']} • {r['Last 5']}</p></div>
                    <div class="big-num">{r['Anytime %']}%</div>
                </div>
                <div class="quick-row"><span>🥇 {r['First Try %']}%</span><span>🔥 2+ {r['2+ %']}%</span><span>🚀 3+ {r['3+ %']}%</span></div>
                <p class="muted">Fair {r['Fair Odds']} • Book {r['Book Odds']} • Edge {r['Edge %']}%</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("## 💰 Value Table")
        st.dataframe(players, use_container_width=True, hide_index=True)

st.markdown("""<div class="navbar"><div class="navitem">🏠<br>Home</div><div class="navitem">✍️<br>Input</div><div class="navitem">📊<br>Picks</div><div class="navitem">💰<br>Value</div></div>""", unsafe_allow_html=True)
st.caption("Oggy's AI Sports Lab v1.3 Manual Live Round Mode")
