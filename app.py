import streamlit as st
import pandas as pd

from src.phase3_setup_engine import load_demo_data, run_phase2_pipeline, setup_status
from src.warehouse_engine import read_warehouse_table
from src.ui_helpers import mobile_header, inject_mobile_css

st.set_page_config(
    page_title="Oggy's AI Sports Lab",
    page_icon="🏉",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_mobile_css()
mobile_header("🏉 Oggy's AI Sports Lab", "NRL AI prediction demo — mobile ready")

st.markdown("""
### Welcome Nathan

This is the clean Streamlit-ready version.

Use the buttons below to:
1. Load demo NRL data.
2. Run the AI prediction engine.
3. View predictions on your phone.
""")

col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 Load Demo Data", use_container_width=True):
        load_demo_data()
        st.success("Demo data loaded.")

with col2:
    if st.button("🧠 Run AI Prediction Engine", use_container_width=True):
        run_phase2_pipeline(sims=1000)
        st.success("AI predictions generated.")

st.markdown("## ✅ App Status")
status = setup_status()
st.dataframe(status, use_container_width=True)

st.markdown("## 🏆 Match Winner Predictions")
ensemble = read_warehouse_table("phase2_ensemble_predictions")
if ensemble.empty:
    st.info("Tap **Load Demo Data**, then **Run AI Prediction Engine**.")
else:
    display_cols = [c for c in [
        "match_id", "predicted_winner", "final_win_probability",
        "agreement_score", "confidence_label", "ensemble_summary"
    ] if c in ensemble.columns]
    st.dataframe(ensemble[display_cols], use_container_width=True)

st.markdown("## 🎯 Top Try Scorer Markets")
markets = read_warehouse_table("phase2_try_market_simulation")
if markets.empty:
    st.info("Run the AI engine to see try scorer predictions.")
else:
    display_cols = [c for c in [
        "player_name", "team_id", "position", "anytime_prob",
        "first_try_prob", "two_plus_prob", "three_plus_prob", "anytime_fair_odds"
    ] if c in markets.columns]
    st.dataframe(markets[display_cols].head(20), use_container_width=True)

st.markdown("## 🧬 Player DNA")
player_dna = read_warehouse_table("phase2_player_dna")
if player_dna.empty:
    st.info("Run the AI engine to see Player DNA.")
else:
    display_cols = [c for c in [
        "player_name", "team_id", "position", "overall_player_dna",
        "try_scoring_dna", "momentum_dna", "confidence_dna", "dna_summary"
    ] if c in player_dna.columns]
    st.dataframe(player_dna[display_cols].head(20), use_container_width=True)

st.markdown("---")
st.caption("Oggy's AI Sports Lab — Streamlit Ready V1")
