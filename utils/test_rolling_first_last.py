
def test_rolling_first_last(values, method, expected):
    # GH#33155
    x = Series(values)
    result = getattr(x.rolling(3), method)()
    expected = Series(expected)
    tm.assert_almost_equal(result, expected)

    x = DataFrame({"A": values})
    result = getattr(x.rolling(3), method)()
    expected = DataFrame({"A": expected})
    tm.assert_almost_equal(result, expected)

