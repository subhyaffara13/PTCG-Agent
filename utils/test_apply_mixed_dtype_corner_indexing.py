
def test_apply_mixed_dtype_corner_indexing():
    df = DataFrame({"A": ["foo"], "B": [1.0]})
    result = df.apply(lambda x: x["A"], axis=1)
    expected = Series(["foo"], index=range(1))
    tm.assert_series_equal(result, expected)

    result = df.apply(lambda x: x["B"], axis=1)
    expected = Series([1.0], index=range(1))
    tm.assert_series_equal(result, expected)

