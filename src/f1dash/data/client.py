import pandas as pd, streamlit as st
from ..config import CACHE_TTL
from .providers import jolpica as provider

def init_session_flags():
    if "offline" not in st.session_state: st.session_state["offline"] = False
    if "last_error" not in st.session_state: st.session_state["last_error"] = ""

def clear_and_rerun():
    st.cache_data.clear()
    st.rerun()

@st.cache_data(ttl=CACHE_TTL)
def get_completed_round(season: str) -> int:
    data = provider.last_results_json(season)
    try:
        return int(data["MRData"]["RaceTable"]["Races"][0]["round"])
    except Exception:
        st.session_state["offline"] = True
        return 0

@st.cache_data(ttl=CACHE_TTL)
def get_schedule(season: str) -> pd.DataFrame:
    data = provider.schedule_json(season)
    races = data.get("MRData", {}).get("RaceTable", {}).get("Races", [])
    rows = [{
        "round": int(r.get("round", 0)),
        "name": r.get("raceName", ""),
        "date": r.get("date"),
        "time": r.get("time", ""),
        "circuit": (r.get("Circuit", {}) or {}).get("circuitName", ""),
        "country": ((r.get("Circuit", {}) or {}).get("Location", {}) or {}).get("country", "")
    } for r in races]
    df = pd.DataFrame(rows).sort_values("round")
    def _dt(row):
        try:
            base = (row.get("date") or "1970-01-01") + "T" + (row.get("time") or "00:00:00Z")
            return pd.to_datetime(base, utc=True)
        except Exception:
            return pd.NaT
    if not df.empty:
        df["datetime_utc"] = df.apply(_dt, axis=1)
    else:
        df["datetime_utc"] = pd.to_datetime([])
    return df

@st.cache_data(ttl=CACHE_TTL)
def get_driver_standings(season: str) -> pd.DataFrame:
    data = provider.driver_standings_json(season)
    lists = data.get("MRData", {}).get("StandingsTable", {}).get("StandingsLists", [])
    if not lists:
        st.session_state["offline"] = True
        return pd.DataFrame(columns=["position","driver_code","driver","nationality","team","points","wins"])
    standings = lists[0].get("DriverStandings", [])
    rows = []
    for d in standings:
        drv = d.get("Driver", {}) or {}
        cons = (d.get("Constructors") or [{}])[0].get("name", "")
        rows.append({
            "position": int(d.get("position", 0) or 0),
            "driver_code": drv.get("code", "") or "",
            "driver": f"{drv.get('givenName','')} {drv.get('familyName','')}".strip(),
            "nationality": drv.get("nationality", "") or "",
            "team": cons,
            "points": float(d.get("points", 0.0) or 0.0),
            "wins": int(d.get("wins", 0) or 0),
        })
    return pd.DataFrame(rows).sort_values("position", na_position="last")

@st.cache_data(ttl=CACHE_TTL)
def get_constructor_standings(season: str) -> pd.DataFrame:
    data = provider.constructor_standings_json(season)
    lists = data.get("MRData", {}).get("StandingsTable", {}).get("StandingsLists", [])
    if not lists:
        st.session_state["offline"] = True
        return pd.DataFrame(columns=["position","team","nationality","points","wins"])
    standings = lists[0].get("ConstructorStandings", [])
    rows = []
    for c in standings:
        cons = c.get("Constructor", {}) or {}
        rows.append({
            "position": int(c.get("position", 0) or 0),
            "team": cons.get("name", "") or "",
            "nationality": cons.get("nationality", "") or "",
            "points": float(c.get("points", 0.0) or 0.0),
            "wins": int(c.get("wins", 0) or 0),
        })
    return pd.DataFrame(rows).sort_values("position", na_position="last")

@st.cache_data(ttl=CACHE_TTL)
def get_all_results_up_to(season: str, round_inclusive: int) -> pd.DataFrame:
    if round_inclusive <= 0:
        return pd.DataFrame(columns=["round","race","driver","driver_code","team","finish","grid","status","points"])
    results = []
    for rnd in range(1, round_inclusive + 1):
        data = provider.round_results_json(season, rnd)
        races = data.get("MRData", {}).get("RaceTable", {}).get("Races", [])
        if not races:
            continue
        r = races[0]
        round_num = int(r.get("round", rnd))
        race_name = r.get("raceName", f"Round {rnd}")
        for res in r.get("Results", []):
            drv = res.get("Driver", {}) or {}
            cons = res.get("Constructor", {}) or {}
            grid = None
            gr = res.get("grid", None)
            if gr not in (None, ""):
                try: grid = int(gr)
                except Exception: grid = None
            results.append({
                "round": round_num,
                "race": race_name,
                "driver": f"{drv.get('givenName','')} {drv.get('familyName','')}".strip(),
                "driver_code": drv.get("code", "") or "",
                "team": cons.get("name", "") or "",
                "finish": res.get("positionText", "") or "",
                "grid": grid,
                "status": res.get("status", "") or "",
                "points": float(res.get("points", 0.0) or 0.0),
            })
    if not results:
        return pd.DataFrame(columns=["round","race","driver","driver_code","team","finish","grid","status","points"])
    return pd.DataFrame(results).sort_values(["round","points"], ascending=[True, False])