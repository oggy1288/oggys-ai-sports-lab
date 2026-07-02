import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta

st.set_page_config(page_title="Oggy's AI Sports Lab", page_icon="🏉", layout="wide", initial_sidebar_state="collapsed")

AEST = timezone(timedelta(hours=10))
MODEL_VERSION = "v2.9.0"

st.markdown("""
<style>
html, body, [class*="css"] {font-size:13px !important;}
.block-container {padding:.4rem .6rem 1rem .6rem; max-width:1000px;}
h1 {font-size:24px !important;} h2 {font-size:18px !important;} h3 {font-size:16px !important;}
.hero{background:linear-gradient(135deg,#06131f,#064e3b,#0f766e);color:white;padding:13px;border-radius:18px;margin-bottom:10px}
.card{padding:11px;border-radius:16px;border:1px solid rgba(148,163,184,.25);background:rgba(15,23,42,.045);margin-bottom:10px}
.dark{padding:12px;border-radius:16px;background:#0f172a;color:white;margin-bottom:10px}
.row{display:flex;justify-content:space-between;gap:10px;align-items:center}
.big{font-size:19px;font-weight:900}.grade{font-size:26px;font-weight:1000}.muted{font-size:12px;opacity:.72}
.count{padding:8px;border-radius:14px;background:#ecfeff;color:#155e75;border:1px solid #a5f3fc;text-align:center;font-weight:900}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:7px;margin-top:7px}.box{padding:8px;border-radius:13px;background:rgba(15,23,42,.06);text-align:center}
.pill{display:inline-block;padding:4px 9px;border-radius:999px;background:#e0f2fe;color:#075985;font-weight:800;font-size:11px}
.nav-note{background:#0f172a;color:white;padding:8px;border-radius:14px;margin-top:10px;text-align:center;font-size:12px}
div.stButton>button{border-radius:14px!important;min-height:42px!important;font-size:13px!important;width:100%!important}
</style>
""", unsafe_allow_html=True)

GAMES = pd.DataFrame([
    {"Game":"Panthers vs Rabbitohs","Home":"Panthers","Away":"Rabbitohs","KickoffAEST":"2026-07-03 19:50","HomeRating":94,"AwayRating":72,"Venue":"BlueBet Stadium","Weather":"Dry","ActualWinner":""},
    {"Game":"Storm vs Broncos","Home":"Storm","Away":"Broncos","KickoffAEST":"2026-07-04 19:35","HomeRating":89,"AwayRating":84,"Venue":"AAMI Park","Weather":"Light rain","ActualWinner":""},
])

PLAYERS = pd.DataFrame([
    {"Player":"Thomas Jenkins","Team":"Panthers","Opponent":"Rabbitohs","Position":"Centre","Match":"Panthers vs Rabbitohs","Jersey":3,"Last5":"2-0-2-0-2","Form":97,"OpponentScore":95,"TeamAttack":96,"WeatherFit":90,"AnytimeOdds":1.61,"FirstOdds":8.00,"OrderOdds":3.00},
    {"Player":"Brian To'o","Team":"Panthers","Opponent":"Rabbitohs","Position":"Winger","Match":"Panthers vs Rabbitohs","Jersey":5,"Last5":"1-0-1-2-0","Form":94,"OpponentScore":91,"TeamAttack":96,"WeatherFit":88,"AnytimeOdds":1.80,"FirstOdds":12.00,"OrderOdds":3.75},
    {"Player":"Xavier Coates","Team":"Storm","Opponent":"Broncos","Position":"Winger","Match":"Storm vs Broncos","Jersey":2,"Last5":"1-1-1-2-1","Form":92,"OpponentScore":87,"TeamAttack":91,"WeatherFit":80,"AnytimeOdds":2.10,"FirstOdds":12.0,"OrderOdds":4.60},
    {"Player":"Selwyn Cobbo","Team":"Broncos","Opponent":"Storm","Position":"Winger","Match":"Storm vs Broncos","Jersey":5,"Last5":"1-0-2-1-0","Form":84,"OpponentScore":81,"TeamAttack":87,"WeatherFit":82,"AnytimeOdds":2.45,"FirstOdds":14.0,"OrderOdds":5.20},
])

def set_screen(name):
    st.session_state.screen = name

def parse_time(x):
    try:
        return datetime.strptime(str(x), "%Y-%m-%d %H:%M").replace(tzinfo=AEST)
    except Exception:
        return None

def kickoff_display(x):
    d = parse_time(x)
    return "Set kickoff" if d is None else d.strftime("%a %d %b, %I:%M %p AEST").replace(" 0", " ")

def countdown(x):
    d = parse_time(x)
    if d is None: return "Set kickoff"
    s = int((d - datetime.now(AEST)).total_seconds())
    if s <= -10800: return "Completed"
    if s <= 0: return "Live"
    days=s//86400; hours=(s%86400)//3600; mins=(s%3600)//60
    return f"{days}d {hours}h {mins}m" if days else (f"{hours}h {mins}m" if hours else f"{mins}m")

def seq_icons(seq):
    m={"0":"0️⃣","1":"1️⃣","2":"2️⃣","3":"3️⃣"}
    return "".join(m.get(i.strip(), i.strip()) for i in str(seq).split("-"))

def strike(seq):
    vals=[int(x) for x in str(seq).split("-") if str(x).strip().isdigit()]
    return 0 if not vals else sum(v>0 for v in vals)/len(vals)*100

def fair(p): return round(1/p,2) if p else 0
def edge(book, fair_odds): return round(((book/fair_odds)-1)*100,1) if fair_odds and book else 0
def grade(score):
    if score >= 90: return "A+"
    if score >= 82: return "A"
    if score >= 74: return "B+"
    if score >= 66: return "B"
    if score >= 55: return "C"
    return "D"

def game_predictions():
    rows=[]
    for _,r in GAMES.iterrows():
        hr=float(r.HomeRating); ar=float(r.AwayRating)
        p=1/(1+np.exp(-((hr-ar+3)/11)))
        winner=r.Home if p>=.5 else r.Away
        prob=p if winner==r.Home else 1-p
        rows.append({**r.to_dict(),"Winner":winner,"Win %":round(prob*100,1),"Kickoff":kickoff_display(r.KickoffAEST),"Countdown":countdown(r.KickoffAEST)})
    return pd.DataFrame(rows)

def player_predictions():
    rows=[]
    for _,r in PLAYERS.iterrows():
        rating = r.Form*.30 + r.OpponentScore*.20 + r.TeamAttack*.25 + r.WeatherFit*.10 + strike(r.Last5)*.15
        anytime = min(.85, max(.04, rating/128))
        first = min(.34, anytime*.24)
        order = min(.68, first + anytime*.33)
        efair, ffair, ofair = fair(anytime), fair(first), fair(order)
        best_edge = max(edge(r.AnytimeOdds, efair), edge(r.FirstOdds, ffair), edge(r.OrderOdds, ofair))
        conf = round(rating*.65 + 95*.35,1)
        meter = round(min(100, max(0, conf*.35 + 95*.25 + best_edge*.40)),1)
        rows.append({**r.to_dict(),"Rating":round(rating,1),"Confidence":conf,"Data":95,"Edge Meter":meter,"Grade":grade(meter),
                     "Anytime %":round(anytime*100,1),"First %":round(first*100,1),"Order %":round(order*100,1),
                     "Anytime Fair":efair,"First Fair":ffair,"Order Fair":ofair,
                     "Anytime Edge":edge(r.AnytimeOdds, efair),"First Edge":edge(r.FirstOdds, ffair),"Order Edge":edge(r.OrderOdds, ofair),
                     "Last5 Icons":seq_icons(r.Last5)})
    return pd.DataFrame(rows)

def nav():
    cols=st.columns(5)
    if cols[0].button("🏠 Home"): set_screen("Home")
    if cols[1].button("🏉 Match"): set_screen("Match Centre")
    if cols[2].button("🎯 Picks"): set_screen("Anytime")
    if cols[3].button("📊 Stats"): set_screen("Accuracy")
    if cols[4].button("☰ More"): set_screen("Menu")

def menu_buttons(prefix=""):
    cols=st.columns(4)
    if cols[0].button("🎯 Anytime", key=prefix+"any"): set_screen("Anytime")
    if cols[1].button("🥇 First Try", key=prefix+"first"): set_screen("First Try")
    if cols[2].button("🏅 Try Order", key=prefix+"order"): set_screen("Try Order")
    if cols[3].button("💰 Value", key=prefix+"value"): set_screen("Value")

def game_card(g):
    st.markdown(f"""
    <div class="card"><div class="row"><div>
    <span class="pill">🏉 Match</span><h3>{g['Game']}</h3>
    <p class="muted">🕒 {g['Kickoff']} • {g['Venue']} • {g['Weather']}</p>
    <p><b>{g['Winner']}</b> {g['Win %']}%</p></div>
    <div class="count">⏳<br>{g['Countdown']}<br><span class="muted">to kickoff</span></div></div></div>
    """, unsafe_allow_html=True)
    if st.button(f"Open {g['Game']} 🏉", key="open_"+g["Game"]):
        st.session_state.selected_match = g["Game"]
        set_screen("Match Centre")

def player_card(r, mode):
    main = {"Anytime":"Anytime %","First Try":"First %","Try Order":"Order %"}.get(mode,"Anytime %")
    st.markdown(f"""
    <div class="card">
    <div class="row"><div>
    <span class="pill">{mode}</span><h3>#{r['Jersey']} {r['Player']}</h3>
    <p class="muted">{r['Team']} vs {r['Opponent']} • {r['Position']}</p></div>
    <div><div class="grade">{r['Grade']}</div><div class="muted">Grade</div></div></div>
    <p class="muted">Last 5: {r['Last5 Icons']}</p>
    <div class="grid">
    <div class="box">🎯<br><b>{r['Anytime %']}%</b><br><span class="muted">${r['AnytimeOdds']}</span></div>
    <div class="box">🥇<br><b>{r['First %']}%</b><br><span class="muted">${r['FirstOdds']}</span></div>
    <div class="box">🏅<br><b>{r['Order %']}%</b><br><span class="muted">${r['OrderOdds']}</span></div>
    </div>
    <p class="muted">Edge {r['Edge Meter']}% • Confidence {r['Confidence']}% • Data {r['Data']}%</p>
    </div>
    """, unsafe_allow_html=True)
    menu_buttons(prefix=f"{r['Player']}_{mode}_")

if "screen" not in st.session_state: st.session_state.screen="Home"
if "selected_match" not in st.session_state: st.session_state.selected_match="Panthers vs Rabbitohs"

st.markdown(f"""<div class="hero"><h1 style="margin:0;">🏉 Oggy's AI Sports Lab</h1><p style="margin:5px 0 0 0;font-size:12px;opacity:.9;">v2.9 Clickable Navigation • {MODEL_VERSION}</p></div>""", unsafe_allow_html=True)
nav()

games=game_predictions()
players=player_predictions()
screen=st.session_state.screen

if screen=="Home":
    st.markdown("## 🏠 Home")
    c1,c2=st.columns(2)
    best=players.sort_values("Edge Meter", ascending=False).iloc[0]
    nextg=games.iloc[0]
    with c1:
        st.markdown(f"<div class='card'><span class='pill'>⚡ Best Edge</span><h3>{best.Player}</h3><div class='big'>{best.Grade}</div><p class='muted'>Edge {best['Edge Meter']}%</p></div>", unsafe_allow_html=True)
        menu_buttons("home_best_")
    with c2:
        st.markdown(f"<div class='card'><span class='pill'>🕒 Next Kickoff</span><h3>{nextg.Game}</h3><div class='big'>{nextg.Countdown}</div><p class='muted'>{nextg.Kickoff}</p></div>", unsafe_allow_html=True)
        if st.button("Open Match Centre 🏉", key="home_match"): 
            st.session_state.selected_match=nextg.Game; set_screen("Match Centre")
    game_card(nextg)

elif screen=="Menu":
    st.markdown("## ☰ Menu")
    cols=st.columns(3)
    pages=["Home","Match Centre","Anytime","First Try","Try Order","Value","Fixtures","Accuracy","Data"]
    for i,p in enumerate(pages):
        if cols[i%3].button(p, key="menu_"+p):
            set_screen(p)

elif screen=="Fixtures":
    st.markdown("## 🕒 Fixtures")
    for _,g in games.iterrows(): game_card(g)

elif screen=="Match Centre":
    st.markdown("## 🏉 Match Centre")
    match_list=games.Game.tolist()
    idx=match_list.index(st.session_state.selected_match) if st.session_state.selected_match in match_list else 0
    selected=st.selectbox("Select match", match_list, index=idx)
    st.session_state.selected_match=selected
    g=games[games.Game==selected].iloc[0]
    st.markdown(f"<div class='dark'><h2>{g.Game}</h2><div class='row'><div><h3>{g.Winner} {g['Win %']}%</h3><p>🕒 {g.Kickoff}</p><p>{g.Venue} • {g.Weather}</p></div><div class='count'>⏳<br>{g.Countdown}<br><span class='muted'>to kickoff</span></div></div></div>", unsafe_allow_html=True)
    menu_buttons("match_top_")
    for _,r in players[players.Match==selected].sort_values("Edge Meter", ascending=False).iterrows():
        player_card(r, "Match Player")

elif screen in ["Anytime","First Try","Try Order"]:
    st.markdown(f"## { {'Anytime':'🎯 Anytime','First Try':'🥇 First Try','Try Order':'🏅 Try Order'}[screen] }")
    sortcol={"Anytime":"Anytime %","First Try":"First %","Try Order":"Order %"}[screen]
    for _,r in players.sort_values(sortcol, ascending=False).iterrows():
        player_card(r, screen)

elif screen=="Value":
    st.markdown("## 💰 Value")
    rows=[]
    for _,r in players.iterrows():
        rows += [
            {"Player":r.Player,"Market":"Anytime","AI %":r["Anytime %"],"Fair Odds":r["Anytime Fair"],"Book Odds":r.AnytimeOdds,"Edge %":r["Anytime Edge"],"Grade":r.Grade},
            {"Player":r.Player,"Market":"First Try","AI %":r["First %"],"Fair Odds":r["First Fair"],"Book Odds":r.FirstOdds,"Edge %":r["First Edge"],"Grade":r.Grade},
            {"Player":r.Player,"Market":"Try Order","AI %":r["Order %"],"Fair Odds":r["Order Fair"],"Book Odds":r.OrderOdds,"Edge %":r["Order Edge"],"Grade":r.Grade},
        ]
    st.dataframe(pd.DataFrame(rows).sort_values("Edge %", ascending=False), use_container_width=True, hide_index=True)

elif screen=="Accuracy":
    st.markdown("## 📊 Accuracy")
    st.info("Accuracy tracking is ready for results entry once actual match results are entered.")

elif screen=="Data":
    st.markdown("## ✍️ Data")
    st.caption("This simplified v2.9 keeps the editor lightweight while navigation is upgraded.")
    st.dataframe(GAMES, use_container_width=True, hide_index=True)
    st.dataframe(PLAYERS, use_container_width=True, hide_index=True)

st.markdown("<div class='nav-note'>Buttons are clickable: Home • Match • Picks • Stats • More • player market icons</div>", unsafe_allow_html=True)
