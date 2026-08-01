
def test_count_lookarounds(any_string_dtype, pat, expected_data):
    # https://github.com/pandas-dev/pandas/issues/60833
    expected_dtype = (
        "float64" if is_object_or_nan_string_dtype(any_string_dtype) else "Int64"
    )
    ser = Series(["aa", "ab", "ba", "bb", None], dtype=any_string_dtype)
    result = ser.str.count(pat)
    expected = Series(expected_data, dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

