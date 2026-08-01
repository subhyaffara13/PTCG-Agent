
def test_rolling_period_index(index, window, func, values):
    # GH: 34225
    ds = Series([0, 1, 2, 3, 4, 5, 6, 7, 8], index=index)
    result = getattr(ds.rolling(window, closed="left"), func)()
    expected = Series(values, index=index)
    tm.assert_series_equal(result, expected)

