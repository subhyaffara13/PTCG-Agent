
def test_fullmatch(any_string_dtype):
    # GH 32806
    ser = Series(
        ["fooBAD__barBAD", "BAD_BADleroybrown", np.nan, "foo"], dtype=any_string_dtype
    )
    result = ser.str.fullmatch(".*BAD[_]+.*BAD")
    if any_string_dtype == "str":
        # NaN propagates as False
        expected = Series([True, False, False, False], dtype=bool)
    else:
        expected_dtype = (
            "object" if is_object_or_nan_string_dtype(any_string_dtype) else "boolean"
        )
        expected = Series([True, False, np.nan, False], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

