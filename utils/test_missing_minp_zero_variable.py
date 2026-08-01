
def test_missing_minp_zero_variable():
    # https://github.com/pandas-dev/pandas/pull/18921
    x = Series(
        [np.nan] * 4,
        index=DatetimeIndex(["2017-01-01", "2017-01-04", "2017-01-06", "2017-01-07"]),
    )
    result = x.rolling(Timedelta("2D"), min_periods=0).sum()
    expected = Series(0.0, index=x.index)
    tm.assert_series_equal(result, expected)

