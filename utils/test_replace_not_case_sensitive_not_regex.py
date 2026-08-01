
def test_replace_not_case_sensitive_not_regex(any_string_dtype):
    # https://github.com/pandas-dev/pandas/issues/41602
    ser = Series(["A.", "a.", "Ab", "ab", np.nan], dtype=any_string_dtype)

    result = ser.str.replace("a", "c", case=False, regex=False)
    expected = Series(["c.", "c.", "cb", "cb", np.nan], dtype=any_string_dtype)
    tm.assert_series_equal(result, expected)

    result = ser.str.replace("a.", "c.", case=False, regex=False)
    expected = Series(["c.", "c.", "Ab", "ab", np.nan], dtype=any_string_dtype)
    tm.assert_series_equal(result, expected)

