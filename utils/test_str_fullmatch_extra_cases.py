
def test_str_fullmatch_extra_cases(any_string_dtype, pat, case, na, exp):
    ser = Series(["abc", "abc$", "$abc", None], dtype=any_string_dtype)
    result = ser.str.fullmatch(pat, case=case, na=na)

    if any_string_dtype == "str":
        # NaN propagates as False
        exp[-1] = False
        expected_dtype = bool
    else:
        expected_dtype = (
            "object" if is_object_or_nan_string_dtype(any_string_dtype) else "boolean"
        )
    expected = Series(exp, dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

