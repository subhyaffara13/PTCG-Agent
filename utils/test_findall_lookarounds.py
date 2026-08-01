
def test_findall_lookarounds(any_string_dtype, pat, expected_data):
    # https://github.com/pandas-dev/pandas/issues/60833
    ser = Series(["aa", "ab", "ba", "bb", None], dtype=any_string_dtype)
    result = ser.str.findall(pat)
    if any_string_dtype == "object":
        null_result = None
    elif any_string_dtype == "str":
        null_result = np.nan
    elif any_string_dtype == "string":
        null_result = pd.NA
    else:
        raise ValueError(f"Unrecognized dtype: {any_string_dtype}")
    expected = Series([*expected_data, null_result])
    tm.assert_series_equal(result, expected)

