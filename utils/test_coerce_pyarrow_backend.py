
def test_coerce_pyarrow_backend():
    # GH 52588
    pa = pytest.importorskip("pyarrow")
    ser = Series(list("12x"), dtype=ArrowDtype(pa.string()))
    result = to_numeric(ser, errors="coerce", dtype_backend="pyarrow")
    expected = Series([1, 2, None], dtype=ArrowDtype(pa.int64()))
    tm.assert_series_equal(result, expected)

