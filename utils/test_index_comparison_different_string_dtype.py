
def test_index_comparison_different_string_dtype(string_dtype_no_object):
    # GH 61099
    idx = Index(["a", "b", "c"])
    s_obj = Series([1, 2, 3], index=idx)
    s_str = Series([4, 5, 6], index=idx.astype(string_dtype_no_object))

    expected = Series([True, True, True], index=["a", "b", "c"])
    result = s_obj < s_str
    assert_series_equal(result, expected)

    result = s_str > s_obj
    expected.index = idx.astype(string_dtype_no_object)
    assert_series_equal(result, expected)

