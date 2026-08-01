
def test_arrow_timestamp_resample(tz):
    # GH 56371
    idx = Series(date_range("2020-01-01", periods=5), dtype="timestamp[ns][pyarrow]")
    if tz is not None:
        idx = idx.dt.tz_localize(tz)
    expected = Series(np.arange(5, dtype=np.float64), index=idx)
    result = expected.resample("1D").mean()
    tm.assert_series_equal(result, expected)

