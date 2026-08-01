
def test_capitalize(data, expected, any_string_dtype):
    s = Series(data, dtype=any_string_dtype)
    result = s.str.capitalize()
    expected = Series(expected, dtype=any_string_dtype)
    tm.assert_series_equal(result, expected)

