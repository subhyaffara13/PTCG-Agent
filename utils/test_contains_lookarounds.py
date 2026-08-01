
def test_contains_lookarounds(any_string_dtype, pat, expected_data, na):
    # https://github.com/pandas-dev/pandas/issues/60833
    if any_string_dtype == "object" and not isinstance(na, bool):
        expected_dtype = "object"
    else:
        expected_dtype = (
            np.bool_ if is_object_or_nan_string_dtype(any_string_dtype) else "boolean"
        )
    if any_string_dtype == "object":
        # The behavior here for `na=pd.NA` looks wrong.
        if (na is lib.no_default or pd.isna(na)) and na is not pd.NA:
            na_result = None
        else:
            na_result = na
    elif na is lib.no_default or pd.isna(na):
        if any_string_dtype == "str":
            na_result = False
        elif any_string_dtype == "string":
            na_result = pd.NA
        else:
            raise ValueError(f"Unrecognized string dtype {any_string_dtype}")
    else:
        na_result = na
    expected_data = expected_data.copy()
    expected_data.append(na_result)
    ser = Series(["aa", "ab", "ba", "bb", None], dtype=any_string_dtype)
    result = ser.str.contains(pat, regex=True, na=na)
    expected = Series(expected_data, dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

