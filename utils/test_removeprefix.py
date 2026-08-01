
def test_removeprefix(any_string_dtype, prefix, expected):
    ser = Series(["ab", "a b c", "bc"], dtype=any_string_dtype)
    result = ser.str.removeprefix(prefix)
    ser_expected = Series(expected, dtype=any_string_dtype)
    tm.assert_series_equal(result, ser_expected)

