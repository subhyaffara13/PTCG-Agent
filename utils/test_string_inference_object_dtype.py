
def test_string_inference_object_dtype(all_parsers, dtype, using_infer_string):
    # GH#56047
    data = """a,b
x,a
y,a
z,a"""
    parser = all_parsers
    with pd.option_context("future.infer_string", True):
        result = parser.read_csv(StringIO(data), dtype=dtype)

    expected_dtype = pd.StringDtype(na_value=np.nan) if dtype is str else object
    expected = DataFrame(
        {
            "a": pd.Series(["x", "y", "z"], dtype=expected_dtype),
            "b": pd.Series(["a", "a", "a"], dtype=expected_dtype),
        },
        columns=pd.Index(["a", "b"], dtype=pd.StringDtype(na_value=np.nan)),
    )
    tm.assert_frame_equal(result, expected)

    with pd.option_context("future.infer_string", True):
        result = parser.read_csv(StringIO(data), dtype={"a": dtype})

    expected = DataFrame(
        {
            "a": pd.Series(["x", "y", "z"], dtype=expected_dtype),
            "b": pd.Series(["a", "a", "a"], dtype=pd.StringDtype(na_value=np.nan)),
        },
        columns=pd.Index(["a", "b"], dtype=pd.StringDtype(na_value=np.nan)),
    )
    tm.assert_frame_equal(result, expected)

