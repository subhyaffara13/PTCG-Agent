
def test_callable_result_dtype_series(keys, agg_index, input, dtype, method):
    # GH 21240
    df = DataFrame({"a": [1], "b": [2], "c": [input]})
    op = getattr(df.groupby(keys)["c"], method)
    result = op(lambda x: x.astype(dtype).iloc[0])
    expected_index = pd.RangeIndex(0, 1) if method == "transform" else agg_index
    expected = Series([df["c"].iloc[0]], index=expected_index, name="c").astype(dtype)
    tm.assert_series_equal(result, expected)

