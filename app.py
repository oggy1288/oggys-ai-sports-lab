import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta
from html import escape

st.set_page_config(page_title="Oggy's AI Sports Lab", page_icon="🏉", layout="wide", initial_sidebar_state="collapsed")

AEST = timezone(timedelta(hours=10))
MODEL_VERSION = "v2.8.0"

st.markdown("""
<style>
html, body, [class*="css"] {font-size:13px !important;}
.block-container {padding-top:.35rem; padding-left:.6rem; padding-right:.6rem; max-width:1050px;}
h1 {font-size:24px !important;} h2 {font-size:18px !important;} h3 {font-size:16px !important;}
.hero {background:linear-gradient(135deg,#06131f,#064e3b,#0f766e);color:white;padding:12px;border-radius:17px;margin-bottom:9px;}
.card {padding:10px;border-radius:15px;border:1px solid rgba(148,163,184,.25);background:rgba(15,23,42,.045);margin-bottom:8px;}
.dark {padding:12px;border-radius:16px;background:#0f172a;color:white;margin-bottom:8px;}
.row {display:flex;justify-content:space-between;gap:8px;align-items:center;}
.big {font-size:18px;font-weight:900;}
.grade {font-size:24px;font-weight:1000;}
.muted {font-size:12px;opacity:.72;}
.count {padding:8px;border-radius:14px;background:#ecfeff;color:#155e75;border:1px solid #a5f3fc;text-align:center;font-weight:900;}
.pill-green {display:inline-block;padding:3px 8px;border-radius:999px;background:#dcfce7;color:#166534;font-weight:700;font-size:11px;}
.pill-yellow {display:inline-block;padding:3px 8px;border-radius:999px;background:#fef3c7;color:#92400e;font-weight:700;font-size:11px;}
.pill-orange {display:inline-block;padding:3px 8px;border-radius:999px;background:#ffedd5;color:#9a3412;font-weight:700;font-size:11px;}
.pill-red {display:inline-block;padding:3px 8px;border-radius:999px;background:#fee2e2;color:#991b1b;font-weight:700;font-size:11px;}
.grid {display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin-top:6px;}
.box {padding:7px;border-radius:12px;background:rgba(15,23,42,.06);text-align:center;}
.nav {background:#0f172a;color:white;padding:8px;border-radius:14px;margin-top:10px;text-align:center;font-size:12px;}
button {border-radius:12px !important;min-height:36px !important;font-size:13px !important;}
</style>
""", unsafe_allow_html=True)

NOW = datetime.now(AEST).strftime("%Y-%m-%d %H:%M AEST")

DEFAULT_GAMES = pd.DataFrame([
    {"Game":"Panthers vs Rabbitohs","Home":"Panthers","Away":"Rabbitohs","KickoffAEST":"2026-07-03 19:50","HomeRating":94,"AwayRating":72,"Venue":"BlueBet","Weather":"Dry","HomeOdds":1.28,"AwayOdds":3.75,"ActualWinner":"","FinalScore":""},
    {"Game":"Storm vs Broncos","Home":"Storm","Away":"Broncos","KickoffAEST":"2026-07-04 19:35","HomeRating":89,"AwayRating":84,"Venue":"AAMI Park","Weather":"Light rain","HomeOdds":1.72,"AwayOdds":2.15,"ActualWinner":"","FinalScore":""},
])

DEFAULT_PLAYERS = pd.DataFrame([
    {"Player":"Thomas Jenkins","Team":"Panthers","Opponent":"Rabbitohs","Position":"Centre","Match":"Panthers vs Rabbitohs","Jersey":3,"Last5Tries":"2-0-2-0-2","VsTeamTries":"2-0-2-0-2","Form":97,"OpponentScore":95,"TeamAttack":96,"WeatherFit":90,"AnytimeOdds":1.90,"FirstOdds":11.0,"TryOrderOdds":4.20,"ActualTries":0,"ActualTryOrders":""},
    {"Player":"Brian To'o","Team":"Panthers","Opponent":"Rabbitohs","Position":"Winger","Match":"Panthers vs Rabbitohs","Jersey":5,"Last5Tries":"1-1-2-1-1","VsTeamTries":"1-1-0-1-2","Form":94,"OpponentScore":91,"TeamAttack":96,"WeatherFit":88,"AnytimeOdds":1.75,"FirstOdds":9.50,"TryOrderOdds":3.75,"ActualTries":0,"ActualTryOrders":""},
    {"Player":"Xavier Coates","Team":"Storm","Opponent":"Broncos","Position":"Winger","Match":"Storm vs Broncos","Jersey":2,"Last5Tries":"1-1-1-2-1","VsTeamTries":"1-0-1-1-0","Form":92,"OpponentScore":87,"TeamAttack":91,"WeatherFit":80,"AnytimeOdds":2.10,"FirstOdds":12.0,"TryOrderOdds":4.60,"ActualTries":0,"ActualTryOrders":""},
    {"Player":"Selwyn Cobbo","Team":"Broncos","Opponent":"Storm","Position":"Winger","Match":"Storm vs Broncos","Jersey":5,"Last5Tries":"1-0-2-1-0","VsTeamTries":"0-1-1-0-1","Form":84,"OpponentScore":81,"TeamAttack":87,"WeatherFit":82,"AnytimeOdds":2.45,"FirstOdds":14.0,"TryOrderOdds":5.20,"ActualTries":0,"ActualTryOrders":""},
])

def parse_kickoff(value):
    raw = str(value or "").strip()
    for fmt in ("%Y-%m-%d %H:%M", "%d/%m/%Y %H:%M", "%Y-%m-%d %I:%M %p", "%d/%m/%Y %I:%M %p"):
        try:
            return datetime.strptime(raw, fmt).replace(tzinfo=AEST)
        except Exception:
            pass
    try:
        dt = datetime.fromisoformat(raw)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=AEST)
        return dt.astimezone(AEST)
    except Exception:
        return None

def kickoff_display(value):
    dt = parse_kickoff(value)
    if not dt:
        return "Kickoff time missing"
    return dt.strftime("%a %d %b %Y, %I:%M %p AEST").replace(" 0", " ")

def countdown(value):
    dt = parse_kickoff(value)
    if not dt:
        return "Set kickoff"
    diff = dt - datetime.now(AEST)
    seconds = int(diff.total_seconds())
    if seconds <= -3*3600:
        return "Completed"
    if seconds <= 0:
        return "Live / Kicked off"
    d = seconds // 86400
    h = (seconds % 86400) // 3600
    m = (seconds % 3600) // 60
    if d:
        return f"{d}d {h}h {m}m"
    if h:
        return f"{h}h {m}m"
    return f"{m}m"

def nums(seq):
    out=[]
    for x in str(seq).replace(",", "-").split("-"):
        try: out.append(int(x.strip()))
        except: pass
    return out or [0,0,0,0,0]

def strike(seq):
    v=nums(seq)
    return sum(1 for x in v if x>=1)/len(v)*100

def fair(p):
    return round(1/p,2) if p>0 else 0

def edge(book, fair_odds):
    try:
        return round(((float(book)/fair_odds)-1)*100,1) if fair_odds>0 and float(book)>0 else 0
    except:
        return 0

def pill(v):
    if v >= 80: return "pill-green"
    if v >= 60: return "pill-yellow"
    if v >= 45: return "pill-orange"
    return "pill-red"

def grade(score):
    if score >= 90: return "A+"
    if score >= 82: return "A"
    if score >= 74: return "B+"
    if score >= 66: return "B"
    if score >= 55: return "C"
    return "D"

def calc_games(df):
    rows=[]
    for _,r in df.iterrows():
        hr=float(r.get("HomeRating",75) or 75); ar=float(r.get("AwayRating",75) or 75)
        p_home=1/(1+np.exp(-((hr-ar+3)/11)))
        winner=r["Home"] if p_home>=.5 else r["Away"]
        prob=p_home if winner==r["Home"] else 1-p_home
        actual=str(r.get("ActualWinner","")).strip()
        result="Pending" if not actual else ("✅ Hit" if actual.lower()==winner.lower() else "❌ Miss")
        rows.append({
            **r.to_dict(),
            "Winner":winner,
            "Win %":round(prob*100,1),
            "Expected Score":f"{r['Home']} {max(round(16+hr*.18-ar*.06+2),6)} - {r['Away']} {max(round(16+ar*.18-hr*.06),6)}",
            "Kickoff Display":kickoff_display(r.get("KickoffAEST","")),
            "Countdown":countdown(r.get("KickoffAEST","")),
            "Winner Result":result,
        })
    return pd.DataFrame(rows).sort_values("KickoffAEST")

def calc_players(df):
    rows=[]
    for _,r in df.iterrows():
        rating = float(r["Form"])*.28 + float(r["OpponentScore"])*.20 + float(r["TeamAttack"])*.22 + float(r["WeatherFit"])*.10 + strike(r["Last5Tries"])*.12 + strike(r["VsTeamTries"])*.08
        anytime=min(.85,max(.04,rating/128))
        first=min(.34,max(.005,anytime*.24))
        order=min(.68,first+anytime*.18+anytime*.15)
        any_f=fair(anytime); first_f=fair(first); order_f=fair(order)
        any_edge=edge(r["AnytimeOdds"], any_f)
        first_edge=edge(r["FirstOdds"], first_f)
        order_edge=edge(r["TryOrderOdds"], order_f)
        data_quality=95 if str(r.get("Player","")).strip() and str(r.get("Last5Tries","")).strip() else 65
        confidence=round(rating*.65+data_quality*.35,1)
        edge_meter=round(min(100,max(0,confidence*.30+data_quality*.25+max(any_edge,first_edge,order_edge)*.45)),1)
        g=grade(edge_meter)
        actual_tries=int(float(r.get("ActualTries",0) or 0))
        orders=set()
        for part in str(r.get("ActualTryOrders","")).replace(" ","").split(","):
            try:
                o=int(part)
                if o in [1,2,3]: orders.add(o)
            except: pass
        rows.append({
            **r.to_dict(),
            "AI Rating":round(rating,1),
            "AI Confidence":confidence,
            "Data Quality":data_quality,
            "AI Edge Meter":edge_meter,
            "Recommendation Grade":g,
            "Anytime %":round(anytime*100,1),
            "First Try %":round(first*100,1),
            "Try Order %":round(order*100,1),
            "Anytime Fair":any_f,
            "First Fair":first_f,
            "Order Fair":order_f,
            "Anytime Edge %":any_edge,
            "First Edge %":first_edge,
            "Order Edge %":order_edge,
            "Anytime Result":"✅ Hit" if actual_tries>=1 else ("❌ Miss" if str(r.get("ActualTries",""))!="" else "Pending"),
            "First Try Result":"✅ Hit" if 1 in orders else ("❌ Miss" if str(r.get("ActualTryOrders","")).strip() else "Pending"),
            "Try Order Result":"✅ Hit" if orders.intersection({1,2,3}) else ("❌ Miss" if str(r.get("ActualTryOrders","")).strip() else "Pending"),
        })
    return pd.DataFrame(rows)

def hit_rate(series):
    done=[x for x in series if x in ["✅ Hit","❌ Miss"]]
    if not done: return 0,0
    return round(sum(1 for x in done if x=="✅ Hit")/len(done)*100,1),len(done)

def game_card(g):
    st.markdown(f"""
    <div class="card">
      <div class="row">
        <div>
          <span class="{pill(float(g['Win %']))}">{escape(g['Winner Result'])}</span>
          <h3>{escape(g['Game'])}</h3>
          <p class="muted">🕒 {escape(g['Kickoff Display'])}</p>
          <p class="muted">{escape(g['Venue'])} • {escape(g['Weather'])}</p>
        </div>
        <div class="count">⏳<br>{escape(g['Countdown'])}<br><span class="muted">to kickoff</span></div>
      </div>
      <p><b>{escape(g['Winner'])}</b> {g['Win %']}% • {escape(g['Expected Score'])}</p>
    </div>
    """, unsafe_allow_html=True)

def player_card(r, market_col, label):
    st.markdown(f"""
    <div class="card">
      <div class="row">
        <div>
          <span class="{pill(float(r[market_col]))}">{label}</span>
          <h3>#{escape(str(r['Jersey']))} {escape(r['Player'])}</h3>
          <p class="muted">{escape(r['Team'])} vs {escape(r['Opponent'])} • {escape(r['Position'])}</p>
        </div>
        <div><div class="grade">{escape(r['Recommendation Grade'])}</div><div class="muted">Grade</div></div>
      </div>
      <div class="grid">
        <div class="box">🎯<br><b>{r['Anytime %']}%</b><br><span class="muted">{r['Anytime Result']}</span></div>
        <div class="box">🥇<br><b>{r['First Try %']}%</b><br><span class="muted">{r['First Try Result']}</span></div>
        <div class="box">🏅<br><b>{r['Try Order %']}%</b><br><span class="muted">{r['Try Order Result']}</span></div>
      </div>
      <p class="muted">Edge {r['AI Edge Meter']}% • Confidence {r['AI Confidence']}% • Data {r['Data Quality']}%</p>
    </div>
    """, unsafe_allow_html=True)

if "games" not in st.session_state:
    st.session_state.games=DEFAULT_GAMES.copy()
if "players" not in st.session_state:
    st.session_state.players=DEFAULT_PLAYERS.copy()

st.markdown(f"""<div class="hero"><h1 style="margin:0;">🏉 Oggy's AI Sports Lab</h1><p style="margin:5px 0 0 0;font-size:12px;opacity:.9;">v2.8 Kickoff Countdown • {MODEL_VERSION}</p></div>""", unsafe_allow_html=True)

screen=st.radio("Navigation", ["🏠 Home","✍️ Data","🕒 Fixtures","🏁 Results","📈 Accuracy","⚡ Edge Meter","🏉 Match Centre","🎯 Anytime","🥇 First Try","🏅 Try Order","💰 Value"], horizontal=True, label_visibility="collapsed")

games=calc_games(st.session_state.games)
players=calc_players(st.session_state.players)

if screen=="✍️ Data":
    st.markdown("## ✍️ Data Editor")
    st.caption("KickoffAEST format: YYYY-MM-DD HH:MM, for example 2026-07-04 19:35")
    st.session_state.games=st.data_editor(st.session_state.games, num_rows="dynamic", use_container_width=True, key="games28")
    st.session_state.players=st.data_editor(st.session_state.players, num_rows="dynamic", use_container_width=True, key="players28")

elif screen=="🕒 Fixtures":
    st.markdown("## 🕒 Fixtures + Countdown")
    st.caption("All kickoff times are shown in AEST.")
    for _,g in games.iterrows():
        game_card(g)

elif screen=="🏁 Results":
    st.markdown("## 🏁 Enter Actual Results")
    st.caption("ActualTryOrders example: 1,3 if the player scored the 1st and 3rd tries.")
    st.session_state.games=st.data_editor(st.session_state.games, num_rows="dynamic", use_container_width=True, key="games_results28")
    st.session_state.players=st.data_editor(st.session_state.players, num_rows="dynamic", use_container_width=True, key="players_results28")

elif screen=="📈 Accuracy":
    st.markdown("## 📈 Accuracy Centre")
    wr,wn=hit_rate(games["Winner Result"]); ar,an=hit_rate(players["Anytime Result"]); fr,fn=hit_rate(players["First Try Result"]); orr,on=hit_rate(players["Try Order Result"])
    c1,c2=st.columns(2); c1.metric("Winner Accuracy",f"{wr}%",f"{wn} graded"); c2.metric("Anytime Accuracy",f"{ar}%",f"{an} graded")
    c3,c4=st.columns(2); c3.metric("First Try Accuracy",f"{fr}%",f"{fn} graded"); c4.metric("Try Order Accuracy",f"{orr}%",f"{on} graded")
    st.dataframe(games[["Game","Kickoff Display","Countdown","Winner","Win %","ActualWinner","Winner Result","FinalScore"]], use_container_width=True, hide_index=True)

elif screen=="⚡ Edge Meter":
    st.markdown("## ⚡ AI Edge Meter")
    for _,r in players.sort_values("AI Edge Meter", ascending=False).iterrows():
        player_card(r,"Anytime %","Edge Meter")

elif screen=="🏠 Home":
    st.markdown("## 🏠 Command Centre")
    next_game=games.iloc[0]
    top_edge=players.sort_values("AI Edge Meter", ascending=False).iloc[0]
    c1,c2=st.columns(2)
    c1.markdown(f"<div class='card'><span class='{pill(top_edge['AI Edge Meter'])}'>⚡ Best Edge</span><h3>{top_edge['Player']}</h3><div class='big'>{top_edge['Recommendation Grade']}</div><p class='muted'>Edge {top_edge['AI Edge Meter']}%</p></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='card'><span class='{pill(next_game['Win %'])}'>🕒 Next Kickoff</span><h3>{next_game['Game']}</h3><div class='big'>{next_game['Countdown']}</div><p class='muted'>{next_game['Kickoff Display']}</p></div>", unsafe_allow_html=True)
    game_card(next_game)

elif screen=="🏉 Match Centre":
    st.markdown("## 🏉 Match Centre")
    selected=st.selectbox("Select match", games["Game"].tolist())
    g=games[games["Game"]==selected].iloc[0]
    st.markdown(f"<div class='dark'><h2>{g['Game']}</h2><div class='row'><div><span class='{pill(g['Win %'])}'>{g['Winner Result']}</span><h3>{g['Winner']} {g['Win %']}%</h3><p>🕒 {g['Kickoff Display']}</p><p>{g['Venue']} • {g['Weather']}</p></div><div class='count'>⏳<br>{g['Countdown']}<br><span class='muted'>to kickoff</span></div></div></div>", unsafe_allow_html=True)
    for _,r in players[players["Match"]==selected].sort_values("AI Edge Meter", ascending=False).iterrows():
        player_card(r,"Anytime %","Match Player")

elif screen=="🎯 Anytime":
    st.markdown("## 🎯 Anytime")
    for _,r in players.sort_values("Anytime %", ascending=False).iterrows():
        player_card(r,"Anytime %","Anytime")

elif screen=="🥇 First Try":
    st.markdown("## 🥇 First Try")
    for _,r in players.sort_values("First Try %", ascending=False).iterrows():
        player_card(r,"First Try %","First Try")

elif screen=="🏅 Try Order":
    st.markdown("## 🏅 Try Order")
    for _,r in players.sort_values("Try Order %", ascending=False).iterrows():
        player_card(r,"Try Order %","Try Order")

elif screen=="💰 Value":
    st.markdown("## 💰 Value")
    rows=[]
    for _,r in players.iterrows():
        rows += [
            {"Player":r["Player"],"Market":"Anytime","AI %":r["Anytime %"],"Fair Odds":r["Anytime Fair"],"Book Odds":r["AnytimeOdds"],"Edge %":r["Anytime Edge %"],"Result":r["Anytime Result"],"Grade":r["Recommendation Grade"]},
            {"Player":r["Player"],"Market":"First Try","AI %":r["First Try %"],"Fair Odds":r["First Fair"],"Book Odds":r["FirstOdds"],"Edge %":r["First Edge %"],"Result":r["First Try Result"],"Grade":r["Recommendation Grade"]},
            {"Player":r["Player"],"Market":"Try Order","AI %":r["Try Order %"],"Fair Odds":r["Order Fair"],"Book Odds":r["TryOrderOdds"],"Edge %":r["Order Edge %"],"Result":r["Try Order Result"],"Grade":r["Recommendation Grade"]},
        ]
    st.dataframe(pd.DataFrame(rows).sort_values("Edge %", ascending=False), use_container_width=True, hide_index=True)

st.markdown("<div class='nav'>🏠 Home • ✍️ Data • 🕒 Fixtures • 🏁 Results • 📈 Accuracy • ⚡ Edge • 🏉 Match • 🎯 Anytime • 🥇 First • 🏅 Order • 💰 Value</div>", unsafe_allow_html=True)
st.caption("Oggy's AI Sports Lab v2.8 — AEST kickoff date/time and countdown.")
