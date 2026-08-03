import re

def test_fullmatch_case_kwarg(any_string_dtype):
    ser = Series(["ab", "AB", "abc", "ABC"], dtype=any_string_dtype)
    expected_dtype = (
        np.bool_ if is_object_or_nan_string_dtype(any_string_dtype) else "boolean"
    )

    expected = Series([True, False, False, False], dtype=expected_dtype)

    result = ser.str.fullmatch("ab", case=True)
    tm.assert_series_equal(result, expected)

    expected = Series([True, True, False, False], dtype=expected_dtype)

    result = ser.str.fullmatch("ab", case=False)
    tm.assert_series_equal(result, expected)

    result = ser.str.fullmatch("ab", flags=re.IGNORECASE)
    tm.assert_series_equal(result, expected)

