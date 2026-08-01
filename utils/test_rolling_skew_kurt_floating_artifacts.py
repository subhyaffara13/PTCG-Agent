
def test_rolling_skew_kurt_floating_artifacts():
    # GH 42064 46431

    sr = Series([1 / 3, 4, 0, 0, 0, 0, 0])
    r = sr.rolling(4)
    result = r.skew()
    expected = Series([np.nan, np.nan, np.nan, 1.9619045191072484, 2.0, 0.0, 0.0])
    tm.assert_series_equal(result, expected)
    result = r.kurt()
    expected = Series([np.nan, np.nan, np.nan, 3.8636048803878786, 4.0, -3.0, -3.0])
    tm.assert_series_equal(result, expected)

