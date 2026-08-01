
def test_match_na_kwarg(any_string_dtype):
    # GH #6609
    s = Series(["a", "b", np.nan], dtype=any_string_dtype)

    result = s.str.match("a", na=False)
    expected_dtype = (
        np.bool_ if is_object_or_nan_string_dtype(any_string_dtype) else "boolean"
    )
    expected = Series([True, False, False], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

    result = s.str.match("a")
    if any_string_dtype == "str":
        # NaN propagates as False
        expected_dtype = bool
        na_value = False
    else:
        expected_dtype = (
            "object" if is_object_or_nan_string_dtype(any_string_dtype) else "boolean"
        )
        na_value = np.nan

    expected = Series([True, False, na_value], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

