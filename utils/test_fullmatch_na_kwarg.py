
def test_fullmatch_na_kwarg(any_string_dtype):
    ser = Series(
        ["fooBAD__barBAD", "BAD_BADleroybrown", np.nan, "foo"], dtype=any_string_dtype
    )
    result = ser.str.fullmatch(".*BAD[_]+.*BAD", na=False)
    expected_dtype = (
        np.bool_ if is_object_or_nan_string_dtype(any_string_dtype) else "boolean"
    )
    expected = Series([True, False, False, False], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

