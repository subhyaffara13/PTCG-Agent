
def test_string_array_zfill(nullable_string_dtype, values, width, expected):
    # GH #61485
    s = Series(values, dtype=nullable_string_dtype)
    result = s.str.zfill(width)
    expected = Series(expected, dtype=nullable_string_dtype)
    tm.assert_series_equal(result, expected)

