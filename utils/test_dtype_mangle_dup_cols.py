
def test_dtype_mangle_dup_cols(all_parsers, dtypes, exp_value):
    # GH#35211
    parser = all_parsers
    data = """a,a\n1,1"""
    dtype_dict = {"a": str, **dtypes}
    # GH#42462
    dtype_dict_copy = dtype_dict.copy()
    result = parser.read_csv(StringIO(data), dtype=dtype_dict)
    expected = DataFrame({"a": ["1"], "a.1": [exp_value]})
    assert dtype_dict == dtype_dict_copy, "dtype dict changed"
    tm.assert_frame_equal(result, expected)

