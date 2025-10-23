from ...config import ERGAST_BASE, SEASON
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

def schedule_json():
    return fetch_json(f"/{SEASON}.json")

def driver_standings_json():
    return fetch_json(f"/{SEASON}/driverStandings.json")

def constructor_standings_json():
    return fetch_json(f"/{SEASON}/constructorStandings.json")

def round_results_json(rnd: int):
    return fetch_json(f"/{SEASON}/{rnd}/results.json")

def last_results_json():
    return fetch_json(f"/{SEASON}/last/results.json")