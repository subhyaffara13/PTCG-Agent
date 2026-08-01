
def test_index_missing(any_string_dtype, method, exp):
    ser = Series(["abcb", "ab", "bcbe", np.nan], dtype=any_string_dtype)
    if is_object_or_nan_string_dtype(any_string_dtype):
        expected_dtype = np.float64
        item = np.nan
    else:
        expected_dtype = "Int64"
        item = NA

    result = getattr(ser.str, method)("b")
    expected = Series([*exp, item], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

