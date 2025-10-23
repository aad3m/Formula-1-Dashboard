from src.f1dash.services.fantasy import summarize_driver_form, compute_fantasy_score

def test_summarize_driver_form(sample_results_df):
    form = summarize_driver_form(sample_results_df, last_n=2)
    assert not form.empty
    assert "recent_avg" in form.columns
    assert set(form["driver"]) == {"Max Verstappen", "Charles Leclerc"}

def test_compute_fantasy_score(sample_results_df):
    form = summarize_driver_form(sample_results_df)
    scored = compute_fantasy_score(form, w_recent=1.0, w_season=1.0, vol_penalty=0.5)
    assert "fantasy_score" in scored.columns
    assert len(scored) == 2
    assert scored["fantasy_score"].dtype in (float, "float64", "float32")