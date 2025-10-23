from ...config import ERGAST_BASE
from ...utils.http import retry_get

def fetch_json(path: str) -> dict:
    url = f"{ERGAST_BASE}{path}"
    r = retry_get(url)
    if r is None:
        return {}
    try:
        return r.json()
    except Exception:
        return {}

def schedule_json(season: str):
    return fetch_json(f"/{season}.json")

def driver_standings_json(season: str):
    return fetch_json(f"/{season}/driverStandings.json")

def constructor_standings_json(season: str):
    return fetch_json(f"/{season}/constructorStandings.json")

def round_results_json(season: str, rnd: int):
    return fetch_json(f"/{season}/{rnd}/results.json")

def last_results_json(season: str):
    return fetch_json(f"/{season}/last/results.json")