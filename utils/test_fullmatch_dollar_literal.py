
def test_fullmatch_dollar_literal(any_string_dtype):
    # GH 56652
    ser = Series(["foo", "foo$foo", np.nan, "foo$"], dtype=any_string_dtype)
    result = ser.str.fullmatch("foo\\$")
    if any_string_dtype == "str":
        # NaN propagates as False
        expected = Series([False, False, False, True], dtype=bool)
    else:
        expected_dtype = (
            "object" if is_object_or_nan_string_dtype(any_string_dtype) else "boolean"
        )
        expected = Series([False, False, np.nan, True], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

