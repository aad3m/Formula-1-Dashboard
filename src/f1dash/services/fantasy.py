import pandas as pd

def summarize_driver_form(df_results: pd.DataFrame, last_n: int = 5) -> pd.DataFrame:
    if df_results.empty:
        return pd.DataFrame(columns=["driver","recent_avg","recent_std","recent_sum","recent_median","season_avg","season_sum","team"])
    max_round = int(df_results["round"].max())
    recent = df_results[df_results["round"] > max_round - last_n]
    recent_stats = recent.groupby("driver", dropna=False)["points"].agg(
        recent_avg="mean", recent_std="std", recent_sum="sum", recent_median="median"
    ).fillna(0.0)
    season_stats = df_results.groupby("driver", dropna=False)["points"].agg(
        season_avg="mean", season_sum="sum"
    )
    teams = (df_results.sort_values("round")
                      .groupby("driver", dropna=False)["team"]
                      .agg(lambda x: x.iloc[-1]))
    form = recent_stats.join(season_stats, how="outer").join(teams, how="left")
    return form.reset_index().fillna(0.0)

def compute_fantasy_score(form: pd.DataFrame, w_recent: float, w_season: float, vol_penalty: float) -> pd.DataFrame:
    if form.empty:
        return pd.DataFrame(columns=["driver","team","recent_avg","season_avg","recent_std","fantasy_score"])
    df = form.copy()
    df["fantasy_score"] = (w_recent * df["recent_avg"] + w_season * df["season_avg"]) - vol_penalty * df["recent_std"]
    return df.sort_values("fantasy_score", ascending=False)