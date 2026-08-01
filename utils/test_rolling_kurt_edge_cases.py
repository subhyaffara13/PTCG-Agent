
def test_rolling_kurt_edge_cases(step):
    expected = Series([np.nan] * 4 + [-3.0])[::step]

    # yields all NaN (0 variance)
    d = Series([1] * 5)
    x = d.rolling(window=5, step=step).kurt()
    tm.assert_series_equal(expected, x)

    # yields all NaN (window too small)
    expected = Series([np.nan] * 5)[::step]
    d = Series(np.random.default_rng(2).standard_normal(5))
    x = d.rolling(window=3, step=step).kurt()
    tm.assert_series_equal(expected, x)

    # yields [NaN, NaN, NaN, 1.224307, 2.671499]
    d = Series([-1.50837035, -0.1297039, 0.19501095, 1.73508164, 0.41941401])
    expected = Series([np.nan, np.nan, np.nan, 1.224307, 2.671499])[::step]
    x = d.rolling(window=4, step=step).kurt()
    tm.assert_series_equal(expected, x)

