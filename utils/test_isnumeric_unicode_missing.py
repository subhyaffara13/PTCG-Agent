
def test_isnumeric_unicode_missing(method, expected, any_string_dtype):
    values = ["A", np.nan, "¼", "★", np.nan, "３", "four"]  # noqa: RUF001
    ser = Series(values, dtype=any_string_dtype)
    if any_string_dtype == "str":
        # NaN propagates as False
        expected = Series(expected, dtype=object).fillna(False).astype(bool)
    else:
        expected_dtype = (
            "object" if is_object_or_nan_string_dtype(any_string_dtype) else "boolean"
        )
        expected = Series(expected, dtype=expected_dtype)
    result = getattr(ser.str, method)()
    tm.assert_series_equal(result, expected)

