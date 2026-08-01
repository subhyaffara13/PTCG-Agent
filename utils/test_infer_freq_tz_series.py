
def test_infer_freq_tz_series(tz_naive_fixture):
    # infer_freq should work with both tz-naive and tz-aware series. See gh-52456
    tz = tz_naive_fixture
    idx = date_range("2021-01-01", "2021-01-04", tz=tz)
    series = idx.to_series().reset_index(drop=True)
    inferred_freq = frequencies.infer_freq(series)
    assert inferred_freq == "D"

