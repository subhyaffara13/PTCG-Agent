
def test_rolling_cov_diff_length():
    # GH 7512
    s1 = Series([1, 2, 3], index=range(3))
    s2 = Series([1, 3], index=range(0, 4, 2))
    result = s1.rolling(window=3, min_periods=2).cov(s2)
    expected = Series([None, None, 2.0])
    tm.assert_series_equal(result, expected)

    s2a = Series([1, None, 3], index=range(3))
    result = s1.rolling(window=3, min_periods=2).cov(s2a)
    tm.assert_series_equal(result, expected)

