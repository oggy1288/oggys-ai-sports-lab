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
.oasl-dark {padding:11px; border-radius:16px; background:#0f172a; color:white; margin-bottom:8px;}
.pill-green {display:inline-block;padding:3px 8px;border-radius:999px;background:#dcfce7;color:#166534;font-weight:700;font-size:11px;}
.pill-yellow {display:inline-block;padding:3px 8px;border-radius:999px;background:#fef3c7;color:#92400e;font-weight:700;font-size:11px;}
.pill-orange {display:inline-block;padding:3px 8px;border-radius:999px;background:#ffedd5;color:#9a3412;font-weight:700;font-size:11px;}
.pill-red {display:inline-block;padding:3px 8px;border-radius:999px;background:#fee2e2;color:#991b1b;font-weight:700;font-size:11px;}
.quick-row {display:flex;justify-content:space-between;gap:8px;align-items:center;}
.big-num {font-size:18px;font-weight:900;}
.muted {font-size:12px;opacity:.72;}
.market-grid {display:grid; grid-template-columns:repeat(3,1fr); gap:6px; margin-top:6px;}
.market-box {padding:7px; border-radius:12px; background:rgba(15,23,42,.06); text-align:center;}
.bar-bg {height:8px;border-radius:999px;background:rgba(148,163,184,.25);overflow:hidden;margin:4px 0 8px 0;}
.bar-fill {height:8px;border-radius:999px;background:#16a34a;}
.nav-note {background:#0f172a;color:white;padding:8px;border-radius:14px;margin-top:10px;text-align:center;font-size:12px;}
button {border-radius:12px !important; min-height:36px !important; font-size:13px !important;}
</style>
""", unsafe_allow_html=True)

DEFAULT_GAMES = pd.DataFrame([
    {"Game":"Panthers vs Rabbitohs","Home":"Panthers","Away":"Rabbitohs","HomeRating":94,"AwayRating":72,"Venue":"BlueBet","Weather":"Dry","HomeOdds":1.28,"AwayOdds":3.75,"HomeRest":7,"AwayRest":6,"HomeInjuryImpact":4,"AwayInjuryImpact":14},
    {"Game":"Storm vs Broncos","Home":"Storm","Away":"Broncos","HomeRating":89,"AwayRating":84,"Venue":"AAMI Park","Weather":"Light rain","HomeOdds":1.72,"AwayOdds":2.15,"HomeRest":6,"AwayRest":7,"HomeInjuryImpact":8,"AwayInjuryImpact":6},
    {"Game":"Cowboys vs Dolphins","Home":"Cowboys","Away":"Dolphins","HomeRating":81,"AwayRating":77,"Venue":"QCB Stadium","Weather":"Humid","HomeOdds":1.82,"AwayOdds":2.02,"HomeRest":8,"AwayRest":6,"HomeInjuryImpact":7,"AwayInjuryImpact":9},
])

DEFAULT_PLAYERS = pd.DataFrame([
    {"Player":"Thomas Jenkins","Team":"Panthers","Opponent":"Rabbitohs","Position":"Centre","Match":"Panthers vs Rabbitohs","Last5":"2-0-2-0-2","Last10":"1-0-1-2-0-2-1-0-2-2","VsTeam":"2-0-2-0-2","VenueHistory":"1-2-1-1-1","Form":97,"OpponentScore":95,"TeamAttack":96,"WeatherFit":90,"TeamNews":94,"RestDays":7,"AnytimeOdds":1.90,"FirstOdds":11.0,"TryOrderOdds":4.20},
    {"Player":"Brian To'o","Team":"Panthers","Opponent":"Rabbitohs","Position":"Winger","Match":"Panthers vs Rabbitohs","Last5":"1-1-2-1-1","Last10":"1-0-1-1-2-1-1-0-1-2","VsTeam":"1-1-0-1-2","VenueHistory":"1-1-1-2-1","Form":94,"OpponentScore":91,"TeamAttack":96,"WeatherFit":88,"TeamNews":94,"RestDays":7,"AnytimeOdds":1.75,"FirstOdds":9.50,"TryOrderOdds":3.75},
    {"Player":"Isaah Yeo","Team":"Panthers","Opponent":"Rabbitohs","Position":"Lock","Match":"Panthers vs Rabbitohs","Last5":"0-1-0-0-1","Last10":"0-0-1-0-0-1-0-0-1-0","VsTeam":"0-0-1-0-1","VenueHistory":"0-1-0-1-0","Form":78,"OpponentScore":82,"TeamAttack":96,"WeatherFit":84,"TeamNews":92,"RestDays":7,"AnytimeOdds":5.50,"FirstOdds":31.0,"TryOrderOdds":12.0},
    {"Player":"Storm Winger","Team":"Storm","Opponent":"Broncos","Position":"Winger","Match":"Storm vs Broncos","Last5":"1-1-1-2-1","Last10":"0-1-1-0-1-1-2-1-0-1","VsTeam":"1-0-1-1-0","VenueHistory":"1-2-0-1-1","Form":92,"OpponentScore":87,"TeamAttack":91,"WeatherFit":80,"TeamNews":89,"RestDays":6,"AnytimeOdds":2.10,"FirstOdds":12.0,"TryOrderOdds":4.60},
    {"Player":"Broncos Winger","Team":"Broncos","Opponent":"Storm","Position":"Winger","Match":"Storm vs Broncos","Last5":"1-0-2-1-0","Last10":"1-0-1-0-2-1-0-1-0-1","VsTeam":"0-1-1-0-1","VenueHistory":"1-0-0-1-1","Form":84,"OpponentScore":81,"TeamAttack":87,"WeatherFit":82,"TeamNews":90,"RestDays":7,"AnytimeOdds":2.45,"FirstOdds":14.0,"TryOrderOdds":5.20},
])

WEIGHTS = {
    "Last5": 0.20,
    "Last10": 0.15,
    "Opponent": 0.15,
    "Venue": 0.10,
    "TeamAttack": 0.10,
    "OpponentWeakness": 0.10,
    "Weather": 0.05,
    "TeamNews": 0.10,
    "RestDays": 0.05,
}

def visual_seq(seq):
    mp = {"0":"0️⃣","1":"1️⃣","2":"2️⃣","3":"3️⃣","4":"4️⃣"}
    return "".join([mp.get(x.strip(), x.strip()) for x in str(seq).replace(",", "-").split("-") if x.strip()])

def seq_values(seq):
    vals = []
    for x in str(seq).replace(",", "-").split("-"):
        try: vals.append(int(x.strip()))
        except Exception: pass
    return vals if vals else [0,0,0,0,0]

def seq_stats(seq):
    vals = seq_values(seq)
    return {
        "avg": sum(vals)/len(vals),
        "strike": sum(1 for v in vals if v >= 1) / len(vals) * 100,
        "two_plus": sum(1 for v in vals if v >= 2) / len(vals) * 100,
        "total": sum(vals),
        "trend": ((sum(vals[-3:])/min(3,len(vals))) - (sum(vals[:3])/min(3,len(vals)))) if len(vals) >= 3 else 0,
    }

def pct_pill(v):
    if v >= 80: return "pill-green"
    if v >= 60: return "pill-yellow"
    if v >= 45: return "pill-orange"
    return "pill-red"

def fair(prob):
    return round(1/prob, 2) if prob > 0 else 0

def value_edge(book, fair_odds):
    try:
        if float(book) <= 0 or fair_odds <= 0: return 0
        return round(((float(book) / fair_odds) - 1) * 100, 1)
    except Exception:
        return 0

def score_from_rest(days):
    try:
        d = float(days)
    except Exception:
        d = 7
    if d >= 8: return 94
    if d >= 7: return 90
    if d >= 6: return 82
    if d >= 5: return 70
    return 58

def calc_factor_scores(row):
    last5 = seq_stats(row.get("Last5",""))
    last10 = seq_stats(row.get("Last10",""))
    vs = seq_stats(row.get("VsTeam",""))
    venue = seq_stats(row.get("VenueHistory",""))
    scores = {
        "Last5": min(100, last5["strike"]*0.65 + last5["avg"]*22 + max(last5["trend"],0)*6),
        "Last10": min(100, last10["strike"]*0.62 + last10["avg"]*20),
        "Opponent": min(100, vs["strike"]*0.65 + vs["avg"]*23),
        "Venue": min(100, venue["strike"]*0.65 + venue["avg"]*20),
        "TeamAttack": float(row.get("TeamAttack",75) or 75),
        "OpponentWeakness": float(row.get("OpponentScore",75) or 75),
        "Weather": float(row.get("WeatherFit",80) or 80),
        "TeamNews": float(row.get("TeamNews",85) or 85),
        "RestDays": score_from_rest(row.get("RestDays",7)),
    }
    overall = sum(scores[k] * WEIGHTS[k] for k in WEIGHTS)
    confidence = (
        min(len(seq_values(row.get("Last5",""))) / 5, 1) * 20 +
        min(len(seq_values(row.get("Last10",""))) / 10, 1) * 15 +
        min(len(seq_values(row.get("VsTeam",""))) / 5, 1) * 18 +
        min(len(seq_values(row.get("VenueHistory",""))) / 5, 1) * 12 +
        scores["TeamNews"] * .15 +
        scores["Weather"] * .10 +
        10
    )
    return scores, round(overall,1), round(min(100, confidence),1)

def calc_players(df):
    rows = []
    for _, r in df.iterrows():
        scores, rating, confidence = calc_factor_scores(r)
        last = seq_stats(r.get("Last5",""))
        vs = seq_stats(r.get("VsTeam",""))
        venue = seq_stats(r.get("VenueHistory",""))
        anytime = min(.85, max(.04, rating/128))
        first = min(.32, max(.01, anytime * (.20 + scores["Last5"]/900 + scores["Opponent"]/1200)))
        second = min(.28, max(.01, anytime * (.18 + scores["TeamAttack"]/1100 + last["strike"]/1500)))
        third = min(.25, max(.01, anytime * (.16 + scores["OpponentWeakness"]/1200 + vs["avg"]/12)))
        order = min(.65, first + second + third)
        any_f, first_f, order_f = fair(anytime), fair(first), fair(order)
        edge_any = value_edge(r.get("AnytimeOdds",0), any_f)
        edge_first = value_edge(r.get("FirstOdds",0), first_f)
        edge_order = value_edge(r.get("TryOrderOdds",0), order_f)
        dna = "Elite Finisher" if rating >= 88 else ("Strong Scorer" if rating >= 78 else ("Situational Value" if rating >= 68 else "Low Sample / Watch"))
        rows.append({
            "Player":r.get("Player",""), "Team":r.get("Team",""), "Opponent":r.get("Opponent",""), "Position":r.get("Position",""), "Match":r.get("Match",""),
            "Last 5":visual_seq(r.get("Last5","")), "Last 10":visual_seq(r.get("Last10","")), "Vs Team":visual_seq(r.get("VsTeam","")), "Venue":visual_seq(r.get("VenueHistory","")),
            "Last5 Avg":round(last["avg"],2), "Last5 Strike %":round(last["strike"],1), "Vs Avg":round(vs["avg"],2), "Vs Strike %":round(vs["strike"],1),
            "Venue Strike %":round(venue["strike"],1), "AI Rating":rating, "AI Confidence":confidence, "Player DNA":dna,
            "Anytime %":round(anytime*100,1), "First Try %":round(first*100,1), "Second Try %":round(second*100,1), "Third Try %":round(third*100,1), "Try Order %":round(order*100,1),
            "Anytime Fair":any_f, "First Fair":first_f, "Order Fair":order_f,
            "Anytime Odds":float(r.get("AnytimeOdds",0) or 0), "First Odds":float(r.get("FirstOdds",0) or 0), "Try Order Odds":float(r.get("TryOrderOdds",0) or 0),
            "Anytime Edge %":edge_any, "First Edge %":edge_first, "Order Edge %":edge_order,
            **{f"Factor {k}":round(v,1) for k,v in scores.items()}
        })
    return pd.DataFrame(rows)

def calc_games(df):
    rows = []
    for _, r in df.iterrows():
        hr, ar = float(r.get("HomeRating",75) or 75), float(r.get("AwayRating",75) or 75)
        home_rest = score_from_rest(r.get("HomeRest",7))
        away_rest = score_from_rest(r.get("AwayRest",7))
        home_injury = max(0, 100 - float(r.get("HomeInjuryImpact",0) or 0))
        away_injury = max(0, 100 - float(r.get("AwayInjuryImpact",0) or 0))
        home_power = hr*.72 + home_rest*.10 + home_injury*.18 + 3
        away_power = ar*.72 + away_rest*.10 + away_injury*.18
        p_home = 1/(1+np.exp(-((home_power-away_power)/11)))
        winner = r.get("Home") if p_home >= .5 else r.get("Away")
        prob = p_home if winner == r.get("Home") else 1-p_home
        hs = max(round(16 + home_power*.18 - away_power*.06 + 2), 6)
        aw = max(round(16 + away_power*.18 - home_power*.06), 6)
        home_fair, away_fair = fair(p_home), fair(1-p_home)
        rows.append({
            "Game":r.get("Game",""), "Home":r.get("Home",""), "Away":r.get("Away",""), "Venue":r.get("Venue",""), "Weather":r.get("Weather",""),
            "Winner":winner, "Win %":round(prob*100,1), "Expected Score":f"{r.get('Home')} {hs} - {r.get('Away')} {aw}",
            "Home Win %":round(p_home*100,1), "Away Win %":round((1-p_home)*100,1), "Home Fair":home_fair, "Away Fair":away_fair,
            "Home Odds":float(r.get("HomeOdds",0) or 0), "Away Odds":float(r.get("AwayOdds",0) or 0),
            "Home Edge %":value_edge(r.get("HomeOdds",0), home_fair), "Away Edge %":value_edge(r.get("AwayOdds",0), away_fair),
            "Home Power":round(home_power,1), "Away Power":round(away_power,1),
            "Confidence":"High" if prob>=.70 else ("Medium" if prob>=.58 else "Low")
        })
    return pd.DataFrame(rows).sort_values("Win %", ascending=False)

def bar(label, value):
    st.markdown(f"<div class='muted'>{label} — {value}%</div><div class='bar-bg'><div class='bar-fill' style='width:{min(max(float(value),0),100)}%'></div></div>", unsafe_allow_html=True)

def player_summary_card(r, main_col, title):
    st.markdown(f"""
    <div class="oasl-card">
      <div class="quick-row">
        <div>
          <span class="{pct_pill(float(r[main_col]))}">{title}</span>
          <h3>{r['Player']}</h3>
          <p class="muted">{r['Team']} vs {r['Opponent']} • {r['Position']} • {r['Player DNA']}</p>
        </div>
        <div class="big-num">{r[main_col]}%</div>
      </div>
      <div class="market-grid">
        <div class="market-box">🥇<br><b>{r['First Try %']}%</b><br><span class="muted">Fair {r['First Fair']}</span></div>
        <div class="market-box">🥈<br><b>{r['Second Try %']}%</b></div>
        <div class="market-box">🥉<br><b>{r['Third Try %']}%</b></div>
      </div>
      <p class="muted">Confidence {r['AI Confidence']}% • Last 5 {r['Last 5']} • Vs {r['Vs Team']}</p>
    </div>
    """, unsafe_allow_html=True)
    with st.expander(f"Why this pick? {r['Player']}"):
        for key in WEIGHTS:
            bar(key, r[f"Factor {key}"])
        st.write(f"AI confidence: {r['AI Confidence']}%")
        st.write(f"Anytime: fair {r['Anytime Fair']}, book {r['Anytime Odds']}, edge {r['Anytime Edge %']}%")
        st.write(f"First try: fair {r['First Fair']}, book {r['First Odds']}, edge {r['First Edge %']}%")
        st.write(f"Try order: fair {r['Order Fair']}, book {r['Try Order Odds']}, edge {r['Order Edge %']}%")

if "games_input" not in st.session_state:
    st.session_state.games_input = DEFAULT_GAMES.copy()
if "players_input" not in st.session_state:
    st.session_state.players_input = DEFAULT_PLAYERS.copy()

st.markdown("""
<div class="oasl-hero">
<h1 style="margin:0;">🏉 Oggy's AI Sports Lab</h1>
<p style="margin:5px 0 0 0;font-size:12px;opacity:.9;">v2.1 Intelligence Engine</p>
</div>
""", unsafe_allow_html=True)

screen = st.radio(
    "Navigation",
    ["🏠 Home", "✍️ Data", "🏉 Match Centre", "👤 Player DNA", "🎯 Anytime", "🥇 First Try", "🏅 Try Order", "💰 Value", "📊 Analytics"],
    horizontal=True,
    label_visibility="collapsed"
)

games = calc_games(st.session_state.games_input)
players = calc_players(st.session_state.players_input)

if screen == "✍️ Data":
    st.markdown("## ✍️ Manual Data Engine")
    st.markdown("### Games")
    st.session_state.games_input = st.data_editor(st.session_state.games_input, num_rows="dynamic", use_container_width=True, key="games_editor_v21")
    st.markdown("### Players / Markets")
    st.caption("Last5, Last10, VsTeam and VenueHistory use dash format: 2-0-2-0-2")
    st.session_state.players_input = st.data_editor(st.session_state.players_input, num_rows="dynamic", use_container_width=True, key="players_editor_v21")
    st.success("Data updates automatically.")

elif screen == "🏠 Home":
    st.markdown("## 🏠 Command Centre")
    top_game = games.iloc[0]
    top_any = players.sort_values("Anytime %", ascending=False).iloc[0]
    top_first = players.sort_values("First Try %", ascending=False).iloc[0]
    value = players.copy()
    value["Best Edge"] = value[["Anytime Edge %","First Edge %","Order Edge %"]].max(axis=1)
    top_value = value.sort_values("Best Edge", ascending=False).iloc[0]
    c1,c2 = st.columns(2)
    with c1:
        st.markdown(f"<div class='oasl-card'><span class='{pct_pill(top_any['Anytime %'])}'>🎯 Best Anytime</span><h3>{top_any['Player']}</h3><div class='big-num'>{top_any['Anytime %']}%</div><p class='muted'>Confidence {top_any['AI Confidence']}%</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='oasl-card'><span class='{pct_pill(top_game['Win %'])}'>🏆 Best Winner</span><h3>{top_game['Winner']}</h3><div class='big-num'>{top_game['Win %']}%</div><p class='muted'>{top_game['Game']}</p></div>", unsafe_allow_html=True)
    c3,c4 = st.columns(2)
    with c3:
        st.markdown(f"<div class='oasl-card'><span class='pill-yellow'>🥇 First Try</span><h3>{top_first['Player']}</h3><div class='big-num'>{top_first['First Try %']}%</div><p class='muted'>Fair {top_first['First Fair']}</p></div>", unsafe_allow_html=True)
    with c4:
        st.markdown(f"<div class='oasl-card'><span class='pill-green'>💰 Best Value</span><h3>{top_value['Player']}</h3><div class='big-num'>+{top_value['Best Edge']}%</div><p class='muted'>Best market edge</p></div>", unsafe_allow_html=True)

elif screen == "🏉 Match Centre":
    st.markdown("## 🏉 Match Centre")
    selected = st.selectbox("Select match", games["Game"].tolist())
    g = games[games["Game"] == selected].iloc[0]
    match_players = players[players["Match"] == selected].sort_values("Anytime %", ascending=False)
    st.markdown(f"""
    <div class="oasl-dark">
      <h2>{g['Game']}</h2>
      <div class="quick-row"><div><span class="{pct_pill(g['Win %'])}">{g['Confidence']}</span><h3>{g['Winner']} {g['Win %']}%</h3><p>{g['Venue']} • {g['Weather']}</p></div><div class="big-num">{g['Expected Score']}</div></div>
    </div>
    """, unsafe_allow_html=True)
    bar(f"{g['Home']} win", g["Home Win %"])
    bar(f"{g['Away']} win", g["Away Win %"])
    st.markdown("### Team power")
    bar(g["Home"], g["Home Power"])
    bar(g["Away"], g["Away Power"])
    st.markdown("### Best players in this match")
    for _, r in match_players.head(4).iterrows():
        player_summary_card(r, "Anytime %", "Anytime")

elif screen == "👤 Player DNA":
    st.markdown("## 👤 Player DNA")
    selected = st.selectbox("Select player", players["Player"].tolist())
    r = players[players["Player"] == selected].iloc[0]
    player_summary_card(r, "Anytime %", "Player DNA")
    st.markdown("### Confidence Breakdown")
    for key in WEIGHTS:
        bar(key, r[f"Factor {key}"])

elif screen == "🎯 Anytime":
    st.markdown("## 🎯 Anytime Rankings")
    for _, r in players.sort_values("Anytime %", ascending=False).iterrows():
        player_summary_card(r, "Anytime %", "Anytime")

elif screen == "🥇 First Try":
    st.markdown("## 🥇 First Try Rankings")
    for _, r in players.sort_values("First Try %", ascending=False).iterrows():
        player_summary_card(r, "First Try %", "First Try")

elif screen == "🏅 Try Order":
    st.markdown("## 🏅 1st / 2nd / 3rd Try Scorer")
    for _, r in players.sort_values("Try Order %", ascending=False).iterrows():
        player_summary_card(r, "Try Order %", "Try Order")

elif screen == "💰 Value":
    st.markdown("## 💰 Value Centre")
    value_rows = []
    for _, r in players.iterrows():
        value_rows += [
            {"Player":r["Player"],"Market":"Anytime","AI %":r["Anytime %"],"Fair Odds":r["Anytime Fair"],"Book Odds":r["Anytime Odds"],"Edge %":r["Anytime Edge %"],"Confidence":r["AI Confidence"]},
            {"Player":r["Player"],"Market":"First Try","AI %":r["First Try %"],"Fair Odds":r["First Fair"],"Book Odds":r["First Odds"],"Edge %":r["First Edge %"],"Confidence":r["AI Confidence"]},
            {"Player":r["Player"],"Market":"Try Order","AI %":r["Try Order %"],"Fair Odds":r["Order Fair"],"Book Odds":r["Try Order Odds"],"Edge %":r["Order Edge %"],"Confidence":r["AI Confidence"]},
        ]
    value = pd.DataFrame(value_rows)
    value["Value Score"] = (value["Edge %"] * .65 + value["Confidence"] * .35).round(1)
    value = value.sort_values("Value Score", ascending=False)
    for _, r in value.head(8).iterrows():
        st.markdown(f"<div class='oasl-card'><div class='quick-row'><div><span class='{pct_pill(float(r['AI %']))}'>{r['Market']}</span><h3>{r['Player']}</h3><p class='muted'>Fair {r['Fair Odds']} • Book {r['Book Odds']} • Confidence {r['Confidence']}%</p></div><div class='big-num'>+{r['Edge %']}%</div></div></div>", unsafe_allow_html=True)
    st.dataframe(value, use_container_width=True, hide_index=True)

elif screen == "📊 Analytics":
    st.markdown("## 📊 Analytics")
    st.markdown("### Top Anytime")
    st.bar_chart(players.set_index("Player")["Anytime %"].sort_values(ascending=False))
    st.markdown("### Confidence")
    st.bar_chart(players.set_index("Player")["AI Confidence"].sort_values(ascending=False))
    st.markdown("### Match Win Probability")
    st.bar_chart(games.set_index("Game")["Win %"].sort_values(ascending=False))

st.markdown("<div class='nav-note'>🏠 Home • ✍️ Data • 🏉 Match • 👤 DNA • 🎯 Anytime • 🥇 First • 🏅 Order • 💰 Value • 📊 Analytics</div>", unsafe_allow_html=True)
st.caption("Oggy's AI Sports Lab v2.1 — weighted intelligence engine.")
