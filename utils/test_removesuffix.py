
def test_removesuffix(any_string_dtype, suffix, expected):
    ser = Series(["ab", "a b c", "bc"], dtype=any_string_dtype)
    result = ser.str.removesuffix(suffix)
    ser_expected = Series(expected, dtype=any_string_dtype)
    tm.assert_series_equal(result, ser_expected)

