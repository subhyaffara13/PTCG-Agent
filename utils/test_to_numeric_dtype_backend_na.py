
def test_to_numeric_dtype_backend_na(val, dtype):
    # GH#50505
    if "pyarrow" in dtype:
        pytest.importorskip("pyarrow")
        dtype_backend = "pyarrow"
    else:
        dtype_backend = "numpy_nullable"
    ser = Series([val, None], dtype=object)
    result = to_numeric(ser, dtype_backend=dtype_backend)
    expected = Series([val, pd.NA], dtype=dtype)
    tm.assert_series_equal(result, expected)

