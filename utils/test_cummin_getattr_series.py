
def test_cummin_getattr_series():
    # GH 15635
    df = DataFrame({"a": [1, 2, 1], "b": [1, 2, 2]})
    result = df.groupby("a").b.cummin()
    expected = Series([1, 2, 1], name="b")
    tm.assert_series_equal(result, expected)

