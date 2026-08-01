
def test_rolling_var_floating_artifact_precision():
    # GH 37051
    s = Series([7, 5, 5, 5])
    result = s.rolling(3).var()
    expected = Series([np.nan, np.nan, 4 / 3, 0])
    tm.assert_series_equal(result, expected, atol=1.0e-15, rtol=1.0e-15)
    # GH 42064
    # new `roll_var` will output 0.0 correctly
    tm.assert_series_equal(result == 0, expected == 0)

