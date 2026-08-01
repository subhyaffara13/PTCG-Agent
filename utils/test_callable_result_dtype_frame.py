
def test_callable_result_dtype_frame(
    keys, agg_index, input_dtype, result_dtype, method
):
    # GH 21240
    df = DataFrame({"a": [1], "b": [2], "c": [True]})
    df["c"] = df["c"].astype(input_dtype)
    op = getattr(df.groupby(keys)[["c"]], method)
    result = op(lambda x: x.astype(result_dtype).iloc[0])
    expected_index = pd.RangeIndex(0, 1) if method == "transform" else agg_index

    if method == "aggregate":
        # _cast_pointwise_result retains the input's dtype where feasible
        if input_dtype == "float32" and result_dtype == "float64":
            result_dtype = "float32"
        if input_dtype == "int32" and result_dtype == "int64":
            result_dtype = "int32"

    expected = DataFrame({"c": [df["c"].iloc[0]]}, index=expected_index).astype(
        result_dtype
    )
    if method == "apply":
        expected.columns.names = [0]
    tm.assert_frame_equal(result, expected)

