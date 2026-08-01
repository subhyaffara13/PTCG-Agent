
def test_str_match_extra_cases(any_string_dtype, pat, case, exp):
    ser = Series(["abc", "Xab"], dtype=any_string_dtype)
    result = ser.str.match(pat, case=case)

    expected_dtype = (
        np.bool_ if is_object_or_nan_string_dtype(any_string_dtype) else "boolean"
    )
    expected = Series(exp, dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

