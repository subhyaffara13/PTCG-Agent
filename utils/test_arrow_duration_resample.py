
def test_arrow_duration_resample():
    # GH 56371
    idx = pd.Index(timedelta_range("1 day", periods=5), dtype="duration[ns][pyarrow]")
    expected = Series(np.arange(5, dtype=np.float64), index=idx)
    result = expected.resample("1D").mean()
    tm.assert_series_equal(result, expected)

