
def test_replace_end_of_string(any_string_dtype):
    # https://github.com/pandas-dev/pandas/pull/63613
    ser = Series(["baz", "bar", "bars", "bar\n"], dtype=any_string_dtype)

    # with dollar sign
    result = ser.str.replace("bar$", "x", regex=True)
    if any_string_dtype == "string" and any_string_dtype.storage == "pyarrow":
        # pyarrow (RE2) only matches $ at the very end of the line
        expected = Series(["baz", "x", "bars", "bar\n"], dtype=any_string_dtype)
    else:
        # python matches $ before or after an ending newline
        expected = Series(["baz", "x", "bars", "x\n"], dtype=any_string_dtype)
    tm.assert_series_equal(result, expected)

    # with \Z (ensure this is translated to \z for pyarrow)
    result = ser.str.replace(r"bar\Z", "x", regex=True)
    expected = Series(["baz", "x", "bars", "bar\n"], dtype=any_string_dtype)
    tm.assert_series_equal(result, expected)

    # ensure finding a literal \Z still works
    ser = Series([r"bar\Z", "bar", "bars", "bar\n"], dtype=any_string_dtype)
    result = ser.str.replace(r"bar\\Z", "x", regex=True)
    expected = Series(["x", "bar", "bars", "bar\n"], dtype=any_string_dtype)
    tm.assert_series_equal(result, expected)

