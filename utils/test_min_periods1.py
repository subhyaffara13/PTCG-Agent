
def test_min_periods1():
    # GH#6795
    df = DataFrame([0, 1, 2, 1, 0], columns=["a"])
    result = df["a"].rolling(3, center=True, min_periods=1).max()
    expected = Series([1.0, 2.0, 2.0, 2.0, 1.0], name="a")
    tm.assert_series_equal(result, expected)

