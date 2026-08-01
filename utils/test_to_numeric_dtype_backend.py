
def test_to_numeric_dtype_backend(val, dtype):
    # GH#50505
    ser = Series([val], dtype=object)
    result = to_numeric(ser, dtype_backend="numpy_nullable")
    expected = Series([val], dtype=dtype)
    tm.assert_series_equal(result, expected)

