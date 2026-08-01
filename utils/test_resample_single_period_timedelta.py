
def test_resample_single_period_timedelta():
    s = Series(list(range(5)), index=timedelta_range("1 day", freq="s", periods=5))
    result = s.resample("2s").sum()
    expected = Series([1, 5, 4], index=timedelta_range("1 day", freq="2s", periods=3))
    tm.assert_series_equal(result, expected)

