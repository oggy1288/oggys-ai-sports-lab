
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta

st.set_page_config(page_title="Oggy's AI Sports Lab", page_icon="🏉", layout="wide", initial_sidebar_state="collapsed")
AEST = timezone(timedelta(hours=10))
MODEL_VERSION = "v3.2.0"

st.markdown("""
<style>
html, body, [class*="css"] {font-size:13px!important}
.block-container{padding:.4rem .55rem 1rem .55rem;max-width:1120px}
h1{font-size:24px!important} h2{font-size:18px!important} h3{font-size:16px!important}
.hero{background:linear-gradient(135deg,#06131f,#064e3b,#0f766e);color:white;padding:13px;border-radius:18px;margin-bottom:10px}
.card{padding:11px;border-radius:16px;border:1px solid rgba(148,163,184,.28);background:rgba(15,23,42,.045);margin-bottom:9px}
.dark{padding:12px;border-radius:16px;background:#0f172a;color:white;margin-bottom:9px}
.row{display:flex;justify-content:space-between;gap:10px;align-items:center}
.big{font-size:19px;font-weight:900}.grade{font-size:24px;font-weight:1000}.muted{font-size:12px;opacity:.72}
.count{padding:8px;border-radius:14px;background:#ecfeff;color:#155e75;border:1px solid #a5f3fc;text-align:center;font-weight:900}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:7px;margin-top:7px}.box{padding:8px;border-radius:13px;background:rgba(15,23,42,.06);text-align:center}
.pill{display:inline-block;padding:4px 9px;border-radius:999px;background:#e0f2fe;color:#075985;font-weight:800;font-size:11px}
.nav-note{background:#0f172a;color:white;padding:8px;border-radius:14px;margin-top:10px;text-align:center;font-size:12px}
div.stButton>button{border-radius:14px!important;min-height:42px!important;font-size:12px!important;width:100%!important}
</style>
""", unsafe_allow_html=True)

COLUMNS=["Sport","Game","Short","Home","Away","KickoffAEST","Venue","Weather","HomeRating","AwayRating","HomeOdds","AwayOdds"]

NRL_GAMES = pd.DataFrame([
    ["NRL","Panthers vs Rabbitohs","PEN v SOU","Panthers","Rabbitohs","2026-07-03 19:50","BlueBet Stadium","Dry",94,72,1.55,2.45],
    ["NRL","Dragons vs Wests Tigers","STI v WST","Dragons","Wests Tigers","2026-07-04 15:00","WIN Stadium","Cloudy",76,70,1.78,2.05],
    ["NRL","Broncos vs Sharks","BRI v CRO","Broncos","Sharks","2026-07-04 17:30","Suncorp Stadium","Dry",86,84,1.88,1.95],
    ["NRL","Eels vs Sea Eagles","PAR v MAN","Eels","Sea Eagles","2026-07-05 14:00","CommBank Stadium","Light rain",74,81,2.25,1.68],
    ["NRL","Knights vs Dolphins","NEW v DOL","Knights","Dolphins","2026-07-05 16:05","McDonald Jones Stadium","Windy",77,79,2.05,1.78],
], columns=COLUMNS)

NRLW_GAMES = pd.DataFrame([
    ["NRLW","Broncos Women vs Titans Women","BRI-W v GLD-W","Broncos Women","Titans Women","2026-07-05 12:00","Suncorp Stadium","Dry",88,82,1.72,2.12],
    ["NRLW","Roosters Women vs Knights Women","SYD-W v NEW-W","Roosters Women","Knights Women","2026-07-06 13:45","Allianz Stadium","Cloudy",90,86,1.80,2.00],
    ["NRLW","Dragons Women vs Sharks Women","STI-W v CRO-W","Dragons Women","Sharks Women","2026-07-06 15:30","WIN Stadium","Light rain",78,80,2.05,1.78],
], columns=COLUMNS)

AFL_GAMES = pd.DataFrame([
    ["AFL","Collingwood vs Carlton","COL v CAR","Collingwood","Carlton","2026-07-03 19:40","MCG","Cool",91,87,1.82,2.02],
    ["AFL","Brisbane Lions vs Sydney","BRI v SYD","Brisbane Lions","Sydney","2026-07-04 16:35","Gabba","Dry",90,88,1.86,1.96],
    ["AFL","Geelong vs Richmond","GEE v RIC","Geelong","Richmond","2026-07-05 15:20","GMHBA Stadium","Windy",84,76,1.55,2.45],
], columns=COLUMNS)

NRL_POS=["Fullback","Winger","Centre","Centre","Winger","Five-eighth","Halfback","Prop","Hooker","Prop","Second Row","Second Row","Lock","Bench","Bench","Bench","Bench"]
AFL_POS=["Midfielder","Midfielder","Mid/Fwd","Ruck","Forward","Key Forward","Small Forward","Midfielder","Defender","Defender","Defender","Key Defender","Forward","Wing","Midfielder","Utility","Ruck/Fwd","Midfielder"]

NRL_TEAMS = {
"Panthers":"Dylan Edwards,Brian To'o,Izack Tago,Paul Alamoti,Thomas Jenkins,Blaize Talagi,Jack Cogger,Moses Leota,Freddy Lussick,Lindsay Smith,Scott Sorensen,Luke Garner,Isaah Yeo,Liam Henry,Lachlan Hubner,Mavrik Geyer,Daine Laurie".split(","),
"Rabbitohs":"Jye Gray,Alex Johnston,Jack Wighton,Campbell Graham,Edward Kosi,Cody Walker,Jamie Humphreys,Tevita Tatola,Peter Mamouzelos,Sean Keppie,Euan Aitken,Keaon Koloamatangi,Tallis Duncan,Siliva Havili,Davvy Moale,Liam Le Blanc,Latrell Mitchell".split(","),
"Dragons":"Tyrell Sloan,Christian Tuipulotu,Moses Suli,Max Feagai,Mat Feagai,Kyle Flanagan,Ben Hunt,Francis Molo,Jacob Liddle,Hame Sele,Jaydn Su'A,Luciano Leilua,Jack de Belin,Blake Lawrie,Raymond Faitala-Mariner,Toby Couchman,Fa'amanu Brown".split(","),
"Wests Tigers":"Jahream Bula,Sunia Turuva,Adam Doueihi,Justin Olam,Charlie Staines,Lachlan Galvin,Jarome Luai,Terrell May,Api Koroisau,Alex Twal,Samuela Fainu,Alex Seyfarth,Fonua Pole,Tallyn Da Silva,Sione Fainu,Tony Sukkar,Latu Fainu".split(","),
"Broncos":"Reece Walsh,Selwyn Cobbo,Kotoni Staggs,Gehamat Shibasaki,Jesse Arthars,Ezra Mam,Adam Reynolds,Payne Haas,Billy Walters,Patrick Carrigan,Jordan Riki,Brendan Piakura,Kobe Hetherington,Tyson Smoothy,Corey Jensen,Xavier Willison,Deine Mariner".split(","),
"Sharks":"William Kennedy,Sione Katoa,Jesse Ramien,KL Iro,Ronaldo Mulitalo,Braydon Trindall,Nicho Hynes,Toby Rudolf,Blayke Brailey,Oregon Kaufusi,Briton Nikora,Teig Wilton,Cameron McInnes,Jack Williams,Tom Hazelton,Siosifa Talakai,Daniel Atkinson".split(","),
"Eels":"Clint Gutherson,Maika Sivo,Will Penisini,Bailey Simonsson,Sean Russell,Dylan Brown,Mitch Moses,Junior Paulo,Joey Lussick,Reagan Campbell-Gillard,Shaun Lane,Bryce Cartwright,J'maine Hopgood,Ryan Matterson,Wiremu Greig,Ofahiki Ogden,Luca Moretti".split(","),
"Sea Eagles":"Tom Trbojevic,Jason Saab,Tolutau Koula,Reuben Garrick,Lehi Hopoate,Luke Brooks,Daly Cherry-Evans,Taniela Paseka,Lachlan Croker,Josh Aloiai,Haumole Olakau'atu,Ben Trbojevic,Jake Trbojevic,Karl Lawton,Ethan Bullemor,Nathan Brown,Corey Waddell".split(","),
"Knights":"Kalyn Ponga,Greg Marzhew,Dane Gagai,Bradman Best,Enari Tuala,Tyson Gamble,Jackson Hastings,Jacob Saifiti,Jayden Brailey,Daniel Saifiti,Dylan Lucas,Kai Pearce-Paul,Adam Elliott,Phoenix Crossland,Leo Thompson,Jack Hetherington,Thomas Cant".split(","),
"Dolphins":"Hamiso Tabuai-Fidow,Jamayne Isaako,Jake Averillo,Herbie Farnworth,Jack Bostock,Kodi Nikorima,Isaiya Katoa,Jesse Bromwich,Jeremy Marshall-King,Tom Flegler,Felise Kaufusi,Connelly Lemuelu,Max Plath,Ray Stone,Mark Nicholls,Kenny Bromwich,Josh Kerr".split(","),
}

NRLW_TEAMS = {
"Broncos Women":"Tamika Upton,Julia Robinson,Mele Hufanga,Shenae Ciesiolka,Hayley Maddick,Ali Brigginshaw,Jada Ferguson,Shannon Mato,Romy Teitzel,Annetta Nuuausala,Amber Hall,Tazmin Rapana,Keilee Joseph,Lavina Gould,Chelsea Lenarduzzi,Zara Canfield,Brianna Clark".split(","),
"Titans Women":"Evania Pelite,Emily Bass,Jaime Chapman,Lauren Brown,Kiana Takairangi,Zara McDonald,Steph Hancock,Shannon Mato,Georgia Hale,Brittany Breayley-Nati,Jessika Elliston,Karina Brown,Rilee Jorgensen,Hailee-Jay Ormond-Maunsell,Destiny Mino-Sinapati,Sienna Lofipo,Georgia Grey".split(","),
"Roosters Women":"Isabelle Kelly,Jess Sergis,Tarryn Aiken,Sam Bremner,Jayme Fressard,Jocelyn Kelleher,Corban Baxter,Simaima Taufa,Olivia Kernick,Keilee Joseph,Millie Boyle,Teuila Fotu-Moala,Mya Hill-Moana,Brydie Parker,Otesa Pule,Shannon Rose,Eliza Lopamaua".split(","),
"Knights Women":"Tamika Upton,Krystal Rota,Yasmin Clydsdale,Hannah Southwell,Jesse Southwell,Kayla Romaniuk,Autumn-Rain Stephens-Daly,Caitlan Johnston,Laishon Albert-Jones,Olivia Higgins,Simone Karpani,Georgia Roche,Lilly-Ann White,Maitua Feterika,Evah McEwen,Sheridan Gallagher,Grace Kukutai".split(","),
"Dragons Women":"Teagan Berry,Raecene McGregor,Tyla King,Kezie Apps,Elsie Albert,Maddison Weatherall,Alexis Tauaneai,Jamie Chapman,Rachael Pearson,Shaylee Bent,Jamilee Bright,Bridget Hoy,Taliah Fuimaono,Bobbi Law,Tara McGrath-West,Charlotte Basham,Bridie Parker".split(","),
"Sharks Women":"Emma Tonegato,Tiana Penitani,Cassie Staples,Jada Taylor,Quincy Dodd,Tayla Preston,Ellie Johnston,Annessa Biddle,Madison Bartlett,Talei Holmes,Georgia Ravics,Chante Temara,Tommy Mikaele,Manilita Takapautolo,Chloe Saunders,Brooke Anderson,Tayla Curtis".split(","),
}

AFL_TEAMS = {
"Collingwood":"Nick Daicos,Josh Daicos,Jordan De Goey,Darcy Cameron,Jamie Elliott,Brody Mihocek,Bobby Hill,Scott Pendlebury,Jack Crisp,Brayden Maynard,Isaac Quaynor,Darcy Moore,Beau McCreery,Patrick Lipinski,Tom Mitchell,Will Hoskin-Elliott,Mason Cox,Finlay Macrae".split(","),
"Carlton":"Charlie Curnow,Harry McKay,Patrick Cripps,Sam Walsh,Adam Cerra,Tom De Koning,Blake Acres,Matthew Cottrell,Nic Newman,Jacob Weitering,Mitch McGovern,Zac Williams,George Hewett,Ollie Hollands,Jesse Motlop,Jack Martin,Corey Durdin,Marc Pittonet".split(","),
"Brisbane Lions":"Lachie Neale,Hugh McCluggage,Cam Rayner,Charlie Cameron,Joe Daniher,Eric Hipwood,Zac Bailey,Josh Dunkley,Dayne Zorko,Oscar McInerney,Jarrod Berry,Brandon Starcevich,Darcy Wilmot,Callum Ah Chee,Lincoln McCarthy,Noah Answerth,Ryan Lester,Kai Lohmann".split(","),
"Sydney":"Isaac Heeney,Chad Warner,Errol Gulden,Tom Papley,Logan McDonald,Will Hayward,Nick Blakey,Callum Mills,Luke Parker,James Rowbottom,Jake Lloyd,Brodie Grundy,Oliver Florent,Justin McInerney,Hayden McLean,Joel Amartey,Lewis Melican,Dane Rampe".split(","),
"Geelong":"Jeremy Cameron,Tom Hawkins,Patrick Dangerfield,Tom Stewart,Gryan Miers,Brad Close,Max Holmes,Mitch Duncan,Mark Blicavs,Jack Bowes,Zach Tuohy,Ollie Henry,Tyson Stengle,Sam De Koning,Rhys Stanley,Tom Atkins,Cam Guthrie,Shaun Mannagh".split(","),
"Richmond":"Tom Lynch,Shai Bolton,Dustin Martin,Tim Taranto,Jacob Hopper,Daniel Rioli,Nick Vlastuin,Noah Balta,Dion Prestia,Liam Baker,Jack Graham,Kamdyn McIntosh,Jayden Short,Maurice Rioli,Tylar Young,Ben Miller,Samson Ryan,Thomson Dow".split(","),
}

def display_time(x):
    d=datetime.strptime(x,"%Y-%m-%d %H:%M").replace(tzinfo=AEST)
    return d.strftime("%a %d %b, %I:%M %p AEST").replace(" 0"," ")
def countdown(x):
    d=datetime.strptime(x,"%Y-%m-%d %H:%M").replace(tzinfo=AEST)
    s=int((d-datetime.now(AEST)).total_seconds())
    if s<=-10800: return "Completed"
    if s<=0: return "Live"
    days=s//86400; h=(s%86400)//3600; m=(s%3600)//60
    return f"{days}d {h}h {m}m" if days else (f"{h}h {m}m" if h else f"{m}m")
def fair(p): return round(1/p,2) if p>0 else 101
def grade(s): return "A+" if s>=90 else "A" if s>=82 else "B+" if s>=74 else "B" if s>=66 else "C" if s>=55 else "D"
def seed_seq(name,maxv=2):
    seed=sum(ord(c) for c in name)
    return [min(maxv,2 if (seed+i*7)%10>=8 else 1 if (seed+i*7)%10>=5 else 0) for i in range(5)]
def icons(vals): return "".join(["0️⃣" if v==0 else "1️⃣" if v==1 else "2️⃣" if v==2 else "3️⃣" for v in vals])
def game_calc(g):
    p=1/(1+np.exp(-((float(g.HomeRating)-float(g.AwayRating)+3)/11)))
    w=g.Home if p>=.5 else g.Away
    return w, round((p if w==g.Home else 1-p)*100,1)

def current_games():
    return NRL_GAMES if st.session_state.sport=="NRL" else NRLW_GAMES if st.session_state.sport=="NRLW" else AFL_GAMES
def team_db():
    if st.session_state.sport=="AFL": return AFL_TEAMS,AFL_POS
    if st.session_state.sport=="NRLW": return NRLW_TEAMS,NRL_POS
    return NRL_TEAMS,NRL_POS

def make_players(g):
    db,pos=team_db()
    rows=[]
    for team,opp,attack in [(g.Home,g.Away,g.HomeRating),(g.Away,g.Home,g.AwayRating)]:
        for i,name in enumerate(db[team]):
            p=pos[i]
            vals=seed_seq(name,3 if g.Sport=="AFL" else 2)
            form=(sum(vals)/5)*26+58
            if g.Sport=="AFL":
                boost=1.24 if p in ["Forward","Key Forward","Small Forward","Ruck/Fwd"] else 1.05 if "Mid" in p else .70
                unit="goals"; market="Anytime Goal"
            else:
                boost=1.16 if p in ["Winger","Centre","Fullback"] else .84 if p in ["Prop","Hooker","Lock"] else .96
                unit="tries"; market="Anytime Try"
            anytime=max(.03,min(.88,(float(attack)*.42+form*.38+80*.20)*boost/135))
            first=max(.004,min(.32,anytime*(.30 if i<=4 else .18)))
            two=max(.002,min(.55,anytime*.36*(sum(vals)/5+0.25)))
            book=round(max(1.05,fair(anytime)*(1+((sum(ord(c) for c in name)%9)-4)/100)),2)
            edge=round(((book/fair(anytime))-1)*100,1)
            conf=round(min(99,float(attack)*.45+form*.40+80*.15),1)
            score=round(max(0,min(100,conf*.45+edge*.40+80*.15)),1)
            rows.append({"Sport":g.Sport,"Player":name,"Team":team,"Opponent":opp,"Jersey":i+1,"Position":p,"Last5":icons(vals),"Season Avg":round(sum(vals)/5,1),"Main Market":market,"Unit":unit,"Anytime %":round(anytime*100,1),"First %":round(first*100,1),"2+ %":round(two*100,1),"Fair Odds":fair(anytime),"Book Odds":book,"Edge %":edge,"Confidence":conf,"Grade":grade(score),"AI Score":score})
    return pd.DataFrame(rows).sort_values("Anytime %",ascending=False)

def nav():
    cols=st.columns(5)
    for col,(label,screen) in zip(cols,[("🏠 Home","Home"),("🏉 Round","Round Hub"),("🎯 Picks","Picks"),("🧩 Multi","Multi Builder"),("📊 Stats","Stats")]):
        if col.button(label): st.session_state.screen=screen
def sport_selector():
    c=st.columns(3)
    if c[0].button("🏉 NRL", use_container_width=True):
        st.session_state.sport="NRL"; st.session_state.selected_game=NRL_GAMES.iloc[0].Game
    if c[1].button("🏉 NRLW", use_container_width=True):
        st.session_state.sport="NRLW"; st.session_state.selected_game=NRLW_GAMES.iloc[0].Game
    if c[2].button("🏉 AFL", use_container_width=True):
        st.session_state.sport="AFL"; st.session_state.selected_game=AFL_GAMES.iloc[0].Game
def tabs():
    games=current_games()
    st.markdown("### Round Games")
    cols=st.columns(len(games))
    for j,(_,g) in enumerate(games.iterrows()):
        if cols[j].button(f"{g.Short}\n{countdown(g.KickoffAEST)}", key=st.session_state.sport+g.Game):
            st.session_state.selected_game=g.Game
    st.session_state.selected_game=st.selectbox("Game dropdown backup",games.Game.tolist(),index=games.Game.tolist().index(st.session_state.selected_game))
def header(g):
    w,p=game_calc(g)
    word="goals" if g.Sport=="AFL" else "tries"
    st.markdown(f"<div class='dark'><div class='row'><div><h2>{g.Game}</h2><p>🕒 {display_time(g.KickoffAEST)}</p><p>{g.Venue} • {g.Weather}</p><h3>{w} {p}%</h3><p class='muted'>Expected {word} model active</p></div><div class='count'>⏳<br>{countdown(g.KickoffAEST)}<br><span class='muted'>to start</span></div></div></div>",unsafe_allow_html=True)
def team_list(g):
    db,pos=team_db()
    c1,c2=st.columns(2)
    for c,team in [(c1,g.Home),(c2,g.Away)]:
        with c:
            st.markdown(f"### {team}")
            st.dataframe(pd.DataFrame({"#":range(1,len(db[team])+1),"Player":db[team],"Position":pos}),use_container_width=True,hide_index=True)
def card(r,label):
    st.markdown(f"<div class='card'><div class='row'><div><span class='pill'>{label}</span><h3>#{r.Jersey} {r.Player}</h3><p class='muted'>{r.Team} vs {r.Opponent} • {r.Position}</p></div><div><div class='grade'>{r.Grade}</div><div class='muted'>Grade</div></div></div><p class='muted'>Last 5 {r.Unit}: {r.Last5} • Season Avg {r['Season Avg']}</p><div class='grid'><div class='box'>🎯<br><b>{r['Anytime %']}%</b><br><span class='muted'>${r['Book Odds']}</span></div><div class='box'>🥇<br><b>{r['First %']}%</b><br><span class='muted'>First</span></div><div class='box'>🔥<br><b>{r['Edge %']}%</b><br><span class='muted'>Edge</span></div></div><p class='muted'>Confidence {r.Confidence}% • Fair ${r['Fair Odds']} • AI Score {r['AI Score']}</p></div>",unsafe_allow_html=True)
def multi_calc(legs):
    if not legs: return 0,0,0
    prob=1; odds=1
    for l in legs: prob*=l["prob"]/100; odds*=l["odds"]
    return round(prob*100,2),round(odds,2),fair(prob)

if "sport" not in st.session_state: st.session_state.sport="NRL"
if "screen" not in st.session_state: st.session_state.screen="Home"
if "selected_game" not in st.session_state: st.session_state.selected_game=NRL_GAMES.iloc[0].Game

st.markdown(f"<div class='hero'><h1>🏉 Oggy's AI Sports Lab</h1><p>v3.2 NRLW Multi-Sport • {MODEL_VERSION}</p></div>",unsafe_allow_html=True)
sport_selector(); nav(); tabs()
games=current_games()
game=games[games.Game==st.session_state.selected_game].iloc[0]
players=make_players(game)
word="Goal" if st.session_state.sport=="AFL" else "Try"

if st.session_state.screen=="Home":
    st.markdown(f"## 🏠 {st.session_state.sport} Home")
    header(game)
    st.markdown(f"### Top 3 {word} Scorers")
    for _,r in players.head(3).iterrows(): card(r,f"Top {word} Scorer")
    st.markdown(f"### Best Value {word} Scorers")
    for _,r in players.sort_values("Edge %",ascending=False).head(3).iterrows(): card(r,"Best Value")
elif st.session_state.screen=="Round Hub":
    st.markdown("## 🏉 Game Breakdown")
    header(game)
    with st.expander("Team Lists / Squads",expanded=True): team_list(game)
    w,p=game_calc(game)
    st.metric("Predicted Winner",w,f"{p}%")
    st.dataframe(players[["Jersey","Player","Team","Position","Last5","Season Avg","Anytime %","First %","2+ %","Book Odds","Edge %","Grade"]],use_container_width=True,hide_index=True)
elif st.session_state.screen=="Picks":
    st.markdown("## 🎯 Picks")
    mode=st.radio("Market",[f"Top 3 {word} Scorers",f"Best Value {word} Scorers",f"First {word}","2+"],horizontal=True)
    sort="Anytime %" if "Top" in mode else "Edge %" if "Value" in mode else "First %" if "First" in mode else "2+ %"
    for _,r in players.sort_values(sort,ascending=False).head(8).iterrows(): card(r,mode)
elif st.session_state.screen=="Multi Builder":
    st.markdown("## 🧩 Multi Builder")
    opts=[f"{r.Player} anytime {word.lower()} (${r['Book Odds']})" for _,r in players.head(12).iterrows()]
    chosen=st.multiselect("Choose same-game legs",opts)
    legs=[]
    for choice in chosen:
        r=players[players.Player==choice.split(" anytime")[0]].iloc[0]
        legs.append({"prob":r["Anytime %"],"odds":r["Book Odds"]})
    p,o,f=multi_calc(legs)
    st.metric("Same Game Multi Probability",f"{p}%")
    st.metric("Book Odds",f"${o}")
    st.metric("AI Fair Odds",f"${f}")
    st.markdown(f"### One {word} Scorer Per Game Multi")
    cross=[]
    for _,g in games.iterrows():
        ps=make_players(g).head(6)
        pick=st.selectbox(g.Game,[f"{r.Player} (${r['Book Odds']})" for _,r in ps.iterrows()],key=st.session_state.sport+"_cross_"+g.Game)
        r=ps[ps.Player==pick.split(" ($")[0]].iloc[0]
        cross.append({"prob":r["Anytime %"],"odds":r["Book Odds"]})
    p,o,f=multi_calc(cross)
    st.metric("Cross-Game Multi Probability",f"{p}%")
    st.metric("Book Odds",f"${o}")
    st.metric("AI Fair Odds",f"${f}")
else:
    st.markdown("## 📊 Stats")
    st.dataframe(players[["Player","Team","Position","Anytime %","First %","2+ %","Edge %","Confidence","Grade"]],use_container_width=True,hide_index=True)

st.markdown("<div class='nav-note'>Multi-sport enabled: NRL + NRLW + AFL • shared Round Hub • sport-specific scorer language • same-game and cross-game multis</div>",unsafe_allow_html=True)
