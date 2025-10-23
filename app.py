import streamlit as st
from src.f1dash.config import APP_TITLE, APP_CAPTION
from src.f1dash.data.client import (
    init_session_flags, clear_and_rerun,
    get_completed_round, get_schedule,
    get_driver_standings, get_constructor_standings,
    get_all_results_up_to,
)
from src.f1dash.ui.layout import render_header, render_kpis, render_tabs

st.set_page_config(page_title=APP_TITLE, page_icon="🏁", layout="wide", initial_sidebar_state="expanded")
init_session_flags()

# Sidebar
st.sidebar.title("⚙️ Controls")
last_n = st.sidebar.slider("Form Window (last N races)", 3, 10, 5, 1)
w_recent = st.sidebar.slider("Weight: Recent Avg", 0.0, 2.0, 1.3, 0.1)
w_season = st.sidebar.slider("Weight: Season Avg", 0.0, 2.0, 0.7, 0.1)
vol_penalty = st.sidebar.slider("Penalty: Volatility (std)", 0.0, 2.0, 0.4, 0.05)
show_per_race = st.sidebar.checkbox("Show per-race table", value=False)
if st.sidebar.button("🔄 Retry (clear cache)"):
    clear_and_rerun()

# Data
completed_round = get_completed_round()
schedule_df = get_schedule()
drivers_df = get_driver_standings()
teams_df = get_constructor_standings()
results_df = get_all_results_up_to(completed_round)

# Derived
TOTAL_RACES = int(schedule_df["round"].max()) if not schedule_df.empty else 24
next_row = schedule_df[schedule_df["round"] == completed_round + 1].head(1) if not schedule_df.empty else None
next_race = next_row["name"].iat[0] if next_row is not None and not next_row.empty else ("Season Complete" if completed_round >= TOTAL_RACES else "—")
next_when = next_row["datetime_utc"].iat[0] if next_row is not None and not next_row.empty else None

# UI
render_header(APP_TITLE, APP_CAPTION)
render_kpis(completed_round, TOTAL_RACES, next_race, next_when, drivers_df, teams_df)
render_tabs(drivers_df, teams_df, results_df, completed_round, last_n, w_recent, w_season, vol_penalty, show_per_race)