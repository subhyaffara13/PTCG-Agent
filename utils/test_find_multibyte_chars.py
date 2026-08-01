
def test_find_multibyte_chars(any_string_dtype):
    # GH#64123 - str.find should return character offsets, not byte offsets
    ser = Series(["ga", "Áa", "永a", "🐍a"], dtype=any_string_dtype)
    expected_dtype = (
        np.int64 if is_object_or_nan_string_dtype(any_string_dtype) else "Int64"
    )

    result = ser.str.find("a")
    expected = Series([1, 1, 1, 1], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

    result = ser.str.find("a", start=1)
    tm.assert_series_equal(result, expected)

