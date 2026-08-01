
def test_to_numeric_dtype_backend_already_nullable(dtype):
    # GH#50505
    if "pyarrow" in dtype:
        pytest.importorskip("pyarrow")
    ser = Series([1, pd.NA], dtype=dtype)
    result = to_numeric(ser, dtype_backend="numpy_nullable")
    expected = Series([1, pd.NA], dtype=dtype)
    tm.assert_series_equal(result, expected)

