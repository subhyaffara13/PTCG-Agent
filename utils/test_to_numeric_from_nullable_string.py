
def test_to_numeric_from_nullable_string(values, nullable_string_dtype, expected):
    # https://github.com/pandas-dev/pandas/issues/37262
    s = Series(values, dtype=nullable_string_dtype)
    result = to_numeric(s)
    tm.assert_series_equal(result, expected)

