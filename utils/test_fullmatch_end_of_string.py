
def test_fullmatch_end_of_string(any_string_dtype):
    # https://github.com/pandas-dev/pandas/pull/63613
    expected_dtype = (
        np.bool_ if is_object_or_nan_string_dtype(any_string_dtype) else "boolean"
    )

    ser = Series(["baz", "bar", "bars", "bar\n"], dtype=any_string_dtype)

    # with dollar sign (for fullmatch, no difference between python and pyarrow)
    result = ser.str.fullmatch("bar$")
    expected = Series([False, True, False, False], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

    # with \Z (ensure this is translated to \z for pyarrow)
    result = ser.str.fullmatch(r"bar\Z")
    tm.assert_series_equal(result, expected)

    # ensure finding a literal \Z still works
    ser = Series([r"bar\Z", "bar", "bars", "bar\n"], dtype=any_string_dtype)
    result = ser.str.fullmatch(r"bar\\Z")
    expected = Series([True, False, False, False], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

