
def test_size_strings(any_string_dtype, using_infer_string):
    # GH#55627
    dtype = any_string_dtype
    df = DataFrame({"a": ["a", "a", "b"], "b": "a"}, dtype=dtype)
    result = df.groupby("a")["b"].size()
    exp_dtype = "Int64" if dtype == "string[pyarrow]" else "int64"
    exp_index_dtype = "str" if using_infer_string and dtype == "object" else dtype
    expected = Series(
        [2, 1],
        index=Index(["a", "b"], name="a", dtype=exp_index_dtype),
        name="b",
        dtype=exp_dtype,
    )
    tm.assert_series_equal(result, expected)

