
def test_rolling_first_last_no_minp(values, method, expected):
    # GH#33155
    x = Series(values)
    result = getattr(x.rolling(3, min_periods=0), method)()
    expected = Series(expected)
    tm.assert_almost_equal(result, expected)

    x = DataFrame({"A": values})
    result = getattr(x.rolling(3, min_periods=0), method)()
    expected = DataFrame({"A": expected})
    tm.assert_almost_equal(result, expected)

