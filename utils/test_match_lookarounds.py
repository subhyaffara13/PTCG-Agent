
def test_match_lookarounds(any_string_dtype, pat, expected_data):
    # https://github.com/pandas-dev/pandas/issues/60833
    if any_string_dtype == "object":
        expected_dtype, null_result = "object", None
    elif any_string_dtype == "str":
        expected_dtype, null_result = "bool", False
    elif any_string_dtype == "string":
        expected_dtype, null_result = "boolean", pd.NA
    else:
        raise ValueError(f"Unrecognized dtype: {any_string_dtype}")
    ser = Series(["aa", "ab", "ba", "bb", None], dtype=any_string_dtype)
    result = ser.str.match(pat)
    expected = Series([*expected_data, null_result], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

