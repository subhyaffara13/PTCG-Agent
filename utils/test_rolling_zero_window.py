
def test_rolling_zero_window():
    # GH 22719
    s = Series(range(1))
    result = s.rolling(0).min()
    expected = Series([np.nan])
    tm.assert_series_equal(result, expected)

