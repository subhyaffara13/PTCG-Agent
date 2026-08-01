
def test_to_numeric_dtype_backend_downcasting_uint(smaller, dtype_backend):
    # GH#50505
    if dtype_backend == "pyarrow":
        pytest.importorskip("pyarrow")
    ser = Series([1, pd.NA], dtype="UInt64")
    result = to_numeric(ser, dtype_backend=dtype_backend, downcast="unsigned")
    expected = Series([1, pd.NA], dtype=smaller)
    tm.assert_series_equal(result, expected)

