
def test_to_numeric_dtype_backend_error(dtype_backend):
    # GH#50505
    ser = Series(["a", "b", ""])
    expected = ser.copy()
    with pytest.raises(ValueError, match="Unable to parse string"):
        to_numeric(ser, dtype_backend=dtype_backend)

    result = to_numeric(ser, dtype_backend=dtype_backend, errors="coerce")
    if dtype_backend == "pyarrow":
        dtype = "double[pyarrow]"
    else:
        dtype = "Float64"
    expected = Series([pd.NA, pd.NA, pd.NA], dtype=dtype)
    tm.assert_series_equal(result, expected)

