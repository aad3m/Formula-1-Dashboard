import sys
import os
import pytest
import pandas as pd

_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

@pytest.fixture
def sample_results_df():
    return pd.DataFrame([
        {"round": 1, "driver": "Max Verstappen", "team": "Red Bull", "points": 25},
        {"round": 2, "driver": "Max Verstappen", "team": "Red Bull", "points": 18},
        {"round": 1, "driver": "Charles Leclerc", "team": "Ferrari", "points": 18},
        {"round": 2, "driver": "Charles Leclerc", "team": "Ferrari", "points": 25},
    ])