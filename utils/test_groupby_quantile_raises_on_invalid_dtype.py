
def test_groupby_quantile_raises_on_invalid_dtype(q, numeric_only):
    df = DataFrame({"a": [1], "b": [2.0], "c": ["x"]})
    if numeric_only:
        result = df.groupby("a").quantile(q, numeric_only=numeric_only)
        expected = df.groupby("a")[["b"]].quantile(q)
        tm.assert_frame_equal(result, expected)
    else:
        msg = "dtype '.*' does not support operation 'quantile'"
        with pytest.raises(TypeError, match=msg):
            df.groupby("a").quantile(q, numeric_only=numeric_only)

