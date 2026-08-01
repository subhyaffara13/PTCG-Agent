
def test_rolling_var_correctness(func, values, window, ddof, expected_values):
    # GH: 37051, 42064, 54518, 52407, 47721
    ts = Series(values)
    result = getattr(ts.rolling(window=window), func)(ddof=ddof)
    if result.last_valid_index():
        result = result[
            result.first_valid_index() : result.last_valid_index() + 1
        ].reset_index(drop=True)
    expected = Series(expected_values)
    tm.assert_series_equal(result, expected, atol=1e-55)
    # GH 42064
    tm.assert_series_equal(result == 0, expected == 0)

