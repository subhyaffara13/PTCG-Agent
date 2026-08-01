
def test_extract_lookarounds(any_string_dtype, pat, expected_data):
    # https://github.com/pandas-dev/pandas/issues/60833
    ser = Series(["aa", "ab", "ba", "bb", None], dtype=any_string_dtype)
    result = ser.str.extract(pat, expand=False)
    if any_string_dtype == "object":
        # object input will preserve None but any result with no matches gets NaN
        expected_data = [np.nan if e is None else e for e in expected_data]
    expected = Series([*expected_data, None], dtype=any_string_dtype)
    tm.assert_series_equal(result, expected)

