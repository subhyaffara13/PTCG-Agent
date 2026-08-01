
def test_setitem_with_different_string_storage():
    # GH#52987
    # Test setitem with values from different string storage type
    pytest.importorskip("pyarrow")

    # Test Series[string[python]].__setitem__(Series[string[pyarrow]])
    ser_python = Series(range(5), dtype="string[python]")
    ser_pyarrow = ser_python.astype("string[pyarrow]")

    ser_python[:2] = ser_pyarrow[:2]
    expected = Series(["0", "1", "2", "3", "4"], dtype="string[python]")
    tm.assert_series_equal(ser_python, expected)

    # Test Series[string[pyarrow]].__setitem__(Series[string[python]])
    ser_pyarrow = Series(range(5), dtype="string[pyarrow]")
    ser_python = ser_pyarrow.astype("string[python]")

    ser_pyarrow[:2] = ser_python[:2]
    expected = Series(["0", "1", "2", "3", "4"], dtype="string[pyarrow]")
    tm.assert_series_equal(ser_pyarrow, expected)

    # Test with slice and missing values
    ser_python = Series(["a", "b", None, "d", "e"], dtype="string[python]")
    ser_pyarrow = Series(["X", "Y", None], dtype="string[pyarrow]")

    ser_python[1:4] = ser_pyarrow
    expected = Series(["a", "X", "Y", NA, "e"], dtype="string[python]")
    tm.assert_series_equal(ser_python, expected)

