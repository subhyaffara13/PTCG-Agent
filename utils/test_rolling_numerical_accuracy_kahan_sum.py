
def test_rolling_numerical_accuracy_kahan_sum():
    # GH: 13254
    df = DataFrame([2.186, -1.647, 0.0, 0.0, 0.0, 0.0], columns=["x"])
    result = df["x"].rolling(3).sum()
    expected = Series([np.nan, np.nan, 0.539, -1.647, 0.0, 0.0], name="x")
    tm.assert_series_equal(result, expected)

