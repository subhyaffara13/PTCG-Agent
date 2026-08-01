
def test_fullmatch_lookarounds(any_string_dtype, pat):
    # https://github.com/pandas-dev/pandas/issues/60833
    # Note: By definition, any match with a lookaround is not a full match.
    if any_string_dtype == "object":
        expected_dtype, null_result = "object", None
    elif any_string_dtype == "str":
        expected_dtype, null_result = "bool", False
    elif any_string_dtype == "string":
        expected_dtype, null_result = "boolean", pd.NA
    else:
        raise ValueError(f"Unrecognized dtype: {any_string_dtype}")
    ser = Series(["aa", "ab", "ba", "bb", None], dtype=any_string_dtype)
    result = ser.str.fullmatch(pat)
    expected = Series(
        [False, True if pat == "ab" else False, False, False, null_result],
        dtype=expected_dtype,
    )
    tm.assert_series_equal(result, expected)

