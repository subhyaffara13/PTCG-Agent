
def test_from_numeric_arrow_dtype(any_numeric_ea_dtype):
    # GH 52425
    pytest.importorskip("pyarrow")
    ser = Series([1, 2], dtype=f"{any_numeric_ea_dtype.lower()}[pyarrow]")
    result = to_datetime(ser)
    expected = Series([1, 2], dtype="datetime64[ns]")
    tm.assert_series_equal(result, expected)


def test_from_numeric_arrow_dtype(any_numeric_ea_dtype):
    # GH 52425
    pytest.importorskip("pyarrow")
    ser = Series([1, 2], dtype=f"{any_numeric_ea_dtype.lower()}[pyarrow]")
    result = to_timedelta(ser)
    expected = Series([1, 2], dtype="timedelta64[ns]")
    tm.assert_series_equal(result, expected)

