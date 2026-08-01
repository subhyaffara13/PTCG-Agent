
def test_series_datetime_index(freq):
    s = Series(date_range("20130101", periods=10, freq=freq))
    inferred = frequencies.infer_freq(s)
    assert inferred == freq

