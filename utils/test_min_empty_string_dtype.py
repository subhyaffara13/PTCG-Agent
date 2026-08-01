
def test_min_empty_string_dtype(func, string_dtype_no_object):
    # GH#55619
    dtype = string_dtype_no_object
    df = DataFrame({"a": ["a"], "b": "a", "c": "a"}, dtype=dtype).iloc[:0]
    result = getattr(df.groupby("a"), func)()
    expected = DataFrame(
        columns=["b", "c"], dtype=dtype, index=pd.Index([], dtype=dtype, name="a")
    )
    tm.assert_frame_equal(result, expected)

