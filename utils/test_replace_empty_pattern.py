
def test_replace_empty_pattern(any_string_dtype):
    # https://github.com/pandas-dev/pandas/issues/64941
    ser = Series(["abcd"], dtype=any_string_dtype)

    result = ser.str.replace("", "")
    expected = Series(["abcd"], dtype=any_string_dtype)
    tm.assert_series_equal(result, expected)

    result = ser.str.replace("", "X")
    expected = Series(["XaXbXcXdX"], dtype=any_string_dtype)
    tm.assert_series_equal(result, expected)

    ser = Series([], dtype=any_string_dtype)
    result = ser.str.replace("", "X")
    expected = Series([], dtype=any_string_dtype)
    tm.assert_series_equal(result, expected)

