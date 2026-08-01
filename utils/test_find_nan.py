
def test_find_nan(any_string_dtype):
    ser = Series(
        ["ABCDEFG", np.nan, "DEFGHIJEF", np.nan, "XXXX"], dtype=any_string_dtype
    )
    if is_object_or_nan_string_dtype(any_string_dtype):
        expected_dtype = np.float64
        item = np.nan
    else:
        expected_dtype = "Int64"
        item = pd.NA

    result = ser.str.find("EF")
    expected = Series([4, item, 1, item, -1], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

    result = ser.str.rfind("EF")
    expected = Series([4, item, 7, item, -1], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

    result = ser.str.find("EF", 3)
    expected = Series([4, item, 7, item, -1], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

    result = ser.str.rfind("EF", 3)
    expected = Series([4, item, 7, item, -1], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

    result = ser.str.find("EF", 3, 6)
    expected = Series([4, item, -1, item, -1], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

    result = ser.str.rfind("EF", 3, 6)
    expected = Series([4, item, -1, item, -1], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

