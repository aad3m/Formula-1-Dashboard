from src.f1dash.data.client import get_schedule

def test_schedule_columns(monkeypatch):
    monkeypatch.setattr("src.f1dash.data.client.provider.schedule_json", lambda: {
        "MRData": {"RaceTable": {"Races": [
            {"round": "1", "raceName": "Bahrain GP", "date": "2025-03-01", "time": "15:00:00Z",
             "Circuit": {"circuitName": "Bahrain Intl", "Location": {"country": "Bahrain"}}}
        ]}}
    })
    df = get_schedule()
    assert {"round", "name", "datetime_utc"}.issubset(df.columns)
    assert df.iloc[0]["country"] == "Bahrain"