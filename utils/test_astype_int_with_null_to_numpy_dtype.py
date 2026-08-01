
def test_astype_int_with_null_to_numpy_dtype(dtype):
    # GH 57093
    ser = pd.Series([1, None], dtype="int64[pyarrow]")
    result = ser.astype(dtype)
    expected = pd.Series([1, None], dtype=dtype)
    tm.assert_series_equal(result, expected)

