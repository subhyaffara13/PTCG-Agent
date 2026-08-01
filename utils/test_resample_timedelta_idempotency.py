
def test_resample_timedelta_idempotency():
    # GH 12072
    index = timedelta_range("0", periods=9, freq="10ms")
    series = Series(range(9), index=index)
    result = series.resample("10ms").mean()
    expected = series.astype(float)
    tm.assert_series_equal(result, expected)

