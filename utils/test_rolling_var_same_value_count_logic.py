
def test_rolling_var_same_value_count_logic(values, window, min_periods, expected):
    # GH 42064.

    expected = Series(expected)
    sr = Series(values)

    # With new algo implemented, result will be set to .0 in rolling var
    # if sufficient amount of consecutively same values are found.
    result_var = sr.rolling(window, min_periods=min_periods).var()

    # use `assert_series_equal` twice to check for equality,
    # because `check_exact=True` will fail in 32-bit tests due to
    # precision loss.

    # 1. result should be close to correct value
    # non-zero values can still differ slightly from "truth"
    # as the result of online algorithm
    tm.assert_series_equal(result_var, expected)
    # 2. zeros should be exactly the same since the new algo takes effect here
    tm.assert_series_equal(expected == 0, result_var == 0)

    # std should also pass as it's just a sqrt of var
    result_std = sr.rolling(window, min_periods=min_periods).std()
    tm.assert_series_equal(result_std, np.sqrt(expected))
    tm.assert_series_equal(expected == 0, result_std == 0)

