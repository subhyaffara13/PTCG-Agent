
def test_repeat_with_null(any_string_dtype, arg, repeat):
    # GH: 31632
    ser = Series(["a", arg], dtype=any_string_dtype)
    result = ser.str.repeat([3, repeat])
    expected = Series(["aaa", None], dtype=any_string_dtype)
    tm.assert_series_equal(result, expected)

