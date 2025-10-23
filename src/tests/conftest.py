import pytest
import pandas as pd

@pytest.fixture
def sample_results_df():
    return pd.DataFrame([
        {"round": 1, "driver": "Max Verstappen", "team": "Red Bull", "points": 25},
        {"round": 2, "driver": "Max Verstappen", "team": "Red Bull", "points": 18},
        {"round": 1, "driver": "Charles Leclerc", "team": "Ferrari", "points": 18},
        {"round": 2, "driver": "Charles Leclerc", "team": "Ferrari", "points": 25},
    ])