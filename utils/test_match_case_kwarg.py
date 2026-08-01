
def test_match_case_kwarg(any_string_dtype):
    values = Series(["ab", "AB", "abc", "ABC"], dtype=any_string_dtype)
    result = values.str.match("ab", case=False)
    expected_dtype = (
        np.bool_ if is_object_or_nan_string_dtype(any_string_dtype) else "boolean"
    )
    expected = Series([True, True, True, True], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

