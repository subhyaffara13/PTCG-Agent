
def test_count_end_of_string(any_string_dtype):
    # https://github.com/pandas-dev/pandas/pull/63613
    expected_dtype = (
        "int64" if is_object_or_nan_string_dtype(any_string_dtype) else "Int64"
    )

    ser = Series(["baz", "bar", "bars", "bar\n"], dtype=any_string_dtype)

    # with dollar sign
    result = ser.str.count("bar$")
    if any_string_dtype == "string" and any_string_dtype.storage == "pyarrow":
        # pyarrow (RE2) only matches $ at the very end of the line
        expected = Series([0, 1, 0, 0], dtype=expected_dtype)
    else:
        # python matches $ before or after an ending newline
        expected = Series([0, 1, 0, 1], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

    # with \Z (ensure this is translated to \z for pyarrow)
    result = ser.str.count(r"bar\Z")
    expected = Series([0, 1, 0, 0], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

    # ensure finding a literal \Z still works
    ser = Series([r"bar\Z", "bar", "bars", "bar\n"], dtype=any_string_dtype)
    result = ser.str.count(r"bar\\Z")
    expected = Series([1, 0, 0, 0], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

