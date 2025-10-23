import pandas as pd, plotly.express as px, streamlit as st
from ..services.fantasy import summarize_driver_form, compute_fantasy_score

def _css():
    st.markdown("""
    <style>
    .block-container { padding-top: 1.2rem; }
    [data-testid="stMetricValue"] { font-size: 1.6rem; }
    .kpi-card { border:1px solid rgba(128,128,128,0.2); border-radius:16px; padding:14px 16px;
                background: rgba(127,127,127,0.07); backdrop-filter: blur(6px); }
    .section-card { border:1px solid rgba(128,128,128,0.2); border-radius:16px; padding:16px 18px; }
    </style>""", unsafe_allow_html=True)

def render_header(title: str, caption: str):
    _css()
    st.title(f"🏁 {title}")
    st.caption(caption)
    if st.session_state.get("offline", False):
        st.warning(
            "Network issue or API unreachable. You're in **Offline Mode**. "
            "Some charts/tables may be empty. Use **Retry** in the sidebar.\n\n"
            f"Last error: `{st.session_state.get('last_error','')}`"
        )

def render_kpis(completed_round, total_races, next_race, next_when, drivers_df, teams_df):
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.metric("Completed Rounds", completed_round, f"of {total_races}")
        st.markdown("</div>", unsafe_allow_html=True)
    with k2:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        if not drivers_df.empty:
            st.metric("Drivers’ Leader", f"{drivers_df.iloc[0]['driver']}", f"{int(drivers_df.iloc[0]['points'])} pts")
        else:
            st.metric("Drivers’ Leader", "—", "")
        st.markdown("</div>", unsafe_allow_html=True)
    with k3:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        if not teams_df.empty:
            st.metric("Constructors’ Leader", f"{teams_df.iloc[0]['team']}", f"{int(teams_df.iloc[0]['points'])} pts")
        else:
            st.metric("Constructors’ Leader", "—", "")
        st.markdown("</div>", unsafe_allow_html=True)
    with k4:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        if next_when is not None and not pd.isna(next_when):
            try: st.metric("Next Race", next_race, pd.to_datetime(next_when).strftime("%b %d"))
            except Exception: st.metric("Next Race", next_race, "")
        else:
            st.metric("Next Race", next_race, "")
        st.markdown("</div>", unsafe_allow_html=True)

def render_tabs(drivers_df, teams_df, results_df, completed_round, last_n, w_recent, w_season, vol_penalty, show_per_race):
    tab_overview, tab_drivers, tab_teams, tab_races, tab_fantasy = st.tabs(
        ["📊 Overview", "👤 Drivers", "🏎️ Teams", "🗺️ Race Tracker", "🧮 Fantasy Helper"]
    )

    with tab_overview:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            if not drivers_df.empty:
                fig = px.bar(drivers_df, x="driver", y="points", color="team",
                             title="Current Driver Points", template="plotly", height=420)
                fig.update_layout(xaxis_title=None, yaxis_title="Points", showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Driver standings unavailable.")
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            if not teams_df.empty:
                fig2 = px.bar(teams_df, x="team", y="points", color="team",
                              title="Constructor Points", template="plotly", height=420)
                fig2.update_layout(xaxis_title=None, yaxis_title="Points", showlegend=False)
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("Constructor standings unavailable.")
            st.markdown("</div>", unsafe_allow_html=True)

    with tab_drivers:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        if not drivers_df.empty:
            team_filter = st.multiselect("Filter by team",
                                         sorted([t for t in drivers_df["team"].dropna().unique() if t]), default=[])
            df = drivers_df.copy()
            if team_filter: df = df[df["team"].isin(team_filter)]
            avg_div = max(1, completed_round) if completed_round else 1
            df["avg_per_race"] = df["points"] / avg_div
            df["projected_24"] = (df["avg_per_race"] * 24).round(1)
            fig3 = px.bar(df.sort_values("points", ascending=False), x="driver", y=["points","projected_24"],
                          barmode="group", title="Current vs Projected (24 races)",
                          template="plotly", height=480, labels={"value":"Points","variable":""})
            st.plotly_chart(fig3, use_container_width=True)
            st.dataframe(
                df[["position","driver","team","points","wins","avg_per_race","projected_24"]]
                .rename(columns={"position":"Pos","driver":"Driver","team":"Team","points":"Pts",
                                 "wins":"Wins","avg_per_race":"Avg/Race","projected_24":"Proj(24)"}),
                use_container_width=True, hide_index=True
            )
        else:
            st.info("Driver tab is limited (no standings).")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_teams:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        if not results_df.empty:
            contrib = results_df.groupby(["team","driver"], dropna=False)["points"].sum().reset_index()
            if not contrib.empty:
                fig4 = px.bar(contrib, x="team", y="points", color="driver",
                              title="Driver Contribution by Team", template="plotly", height=520)
                fig4.update_layout(xaxis_title=None, yaxis_title="Season Points")
                st.plotly_chart(fig4, use_container_width=True)
            else:
                st.info("Not enough race result data to show contributions.")
        else:
            st.info("Team contributions unavailable.")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_races:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        if not results_df.empty:
            cumulative = results_df.groupby(["driver","round"], dropna=False)["points"].sum().reset_index()
            if not cumulative.empty:
                cumulative["cum_points"] = cumulative.groupby("driver", dropna=False)["points"].cumsum()
                totals = cumulative.groupby("driver", dropna=False)["cum_points"].max().sort_values(ascending=False).head(10).index
                top10 = cumulative[cumulative["driver"].isin(totals)]
                if not top10.empty:
                    fig5 = px.line(top10, x="round", y="cum_points", color="driver",
                                   title="Cumulative Points by Round (Top 10)", template="plotly", markers=True, height=520)
                    fig5.update_layout(xaxis_title="Round", yaxis_title="Cumulative Points")
                    st.plotly_chart(fig5, use_container_width=True)
            # optional table
            if show_per_race:
                st.dataframe(
                    results_df.sort_values(["round","points"], ascending=[True, False]),
                    use_container_width=True, hide_index=True
                )
        else:
            st.info("Race tracker unavailable.")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_fantasy:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        form = summarize_driver_form(results_df, last_n=last_n)
        scored = compute_fantasy_score(form, w_recent=w_recent, w_season=w_season, vol_penalty=vol_penalty)
        topn = st.slider("Show Top N", 5, 20, 12, 1)
        st.subheader("Recommended Picks (tunable score)")
        st.caption("Score = recent_weight*recent_avg + season_weight*season_avg − volatility_penalty*recent_std")
        if not scored.empty:
            st.dataframe(
                scored.head(topn)[["driver","team","recent_avg","season_avg","recent_std","fantasy_score"]]
                .rename(columns={"driver":"Driver","team":"Team","recent_avg":"Recent Avg",
                                 "season_avg":"Season Avg","recent_std":"Volatility (std)","fantasy_score":"Score"}),
                use_container_width=True, hide_index=True
            )
            bubble = "season_sum" if "season_sum" in scored.columns else None
            fig6 = px.scatter(scored, x="recent_std", y="recent_avg", size=bubble, color="team",
                              hover_name="driver", template="plotly", height=520,
                              title="Form vs Volatility (bubble ~ season total)")
            fig6.update_layout(xaxis_title="Volatility (std) – lower is steadier", yaxis_title="Recent Avg (last N)")
            st.plotly_chart(fig6, use_container_width=True)
        else:
            st.info("Fantasy helper needs recent race data.")
        st.markdown("</div>", unsafe_allow_html=True)