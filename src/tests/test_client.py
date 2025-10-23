import pandas as pd
import pytest
from src.f1dash.data import client

@pytest.fixture
def fake_standings(monkeypatch):
    def fake_driver_standings_json():
        return {
            "MRData": {
                "StandingsTable": {
                    "StandingsLists": [{
                        "DriverStandings": [{
                            "position": "1",
                            "points": "100",
                            "wins": "5",
                            "Driver": {"givenName": "Max", "familyName": "Verstappen", "code": "VER", "nationality": "Dutch"},
                            "Constructors": [{"name": "Red Bull"}]
                        }]
                    }]
                }
            }
        }
    monkeypatch.setattr(client.provider, "driver_standings_json", fake_driver_standings_json)

def test_get_driver_standings(fake_standings):
    df = client.get_driver_standings()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert df.iloc[0]["driver"] == "Max Verstappen"
    assert df.iloc[0]["team"] == "Red Bull"