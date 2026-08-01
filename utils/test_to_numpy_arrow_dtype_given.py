
def test_to_numpy_arrow_dtype_given():
    # GH#57121
    ser = Series([1, NA], dtype="int64[pyarrow]")
    result = ser.to_numpy(dtype="float64")
    expected = np.array([1.0, np.nan])
    tm.assert_numpy_array_equal(result, expected)

