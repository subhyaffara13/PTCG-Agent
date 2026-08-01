
def test_string_array_boolean_array(nullable_string_dtype, method, expected):
    s = Series(["a", None, "1"], dtype=nullable_string_dtype)
    result = getattr(s.str, method)()
    expected = Series(expected, dtype="boolean")
    tm.assert_series_equal(result, expected)

