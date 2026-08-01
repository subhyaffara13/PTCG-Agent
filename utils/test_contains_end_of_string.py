
def test_contains_end_of_string(any_string_dtype):
    # https://github.com/pandas-dev/pandas/pull/63613
    expected_dtype = (
        np.bool_ if is_object_or_nan_string_dtype(any_string_dtype) else "boolean"
    )

    ser = Series(["baz", "bar", "bars", "bar\n"], dtype=any_string_dtype)

    # with dollar sign
    result = ser.str.contains("bar$")
    if any_string_dtype == "string" and any_string_dtype.storage == "pyarrow":
        # pyarrow (RE2) only matches $ at the very end of the line
        expected = Series([False, True, False, False], dtype=expected_dtype)
    else:
        # python matches $ before or after an ending newline
        expected = Series([False, True, False, True], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

    # with \Z (ensure this is translated to \z for pyarrow)
    result = ser.str.contains(r"bar\Z")
    expected = Series([False, True, False, False], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

    # ensure finding a literal \Z still works
    ser = Series(
        ["bar", r"bar{}".format("\\"), r"bar\Z", r"bar\\Z", "bars", "bar\n"],
        dtype=any_string_dtype,
    )

    result = ser.str.contains(r"bar\\Z")
    expected = Series([False, False, True, False, False, False], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

    result = ser.str.contains(r"bar\\\Z")
    expected = Series([False, True, False, False, False, False], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

    result = ser.str.contains(r"bar\\\\Z")
    expected = Series([False, False, False, True, False, False], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

