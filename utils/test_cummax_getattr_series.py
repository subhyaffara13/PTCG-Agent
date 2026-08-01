
def test_cummax_getattr_series():
    # GH 15635
    df = DataFrame({"a": [1, 2, 1], "b": [2, 1, 1]})
    result = df.groupby("a").b.cummax()
    expected = Series([2, 1, 2], name="b")
    tm.assert_series_equal(result, expected)

