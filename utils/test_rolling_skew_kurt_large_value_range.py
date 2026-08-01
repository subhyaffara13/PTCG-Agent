
def test_rolling_skew_kurt_large_value_range(method, data, values):
    # GH: 37557, 47461, 61416
    s = Series(data)
    result = getattr(s.rolling(4), method)()
    expected = Series(values)
    tm.assert_series_equal(result, expected)

