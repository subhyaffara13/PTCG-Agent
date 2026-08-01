
def test_drop_with_ignore_errors():
    # errors='ignore'
    ser = Series(range(3), index=list("abc"))
    result = ser.drop("bc", errors="ignore")
    tm.assert_series_equal(result, ser)
    result = ser.drop(["a", "d"], errors="ignore")
    expected = ser.iloc[1:]
    tm.assert_series_equal(result, expected)

    # GH 8522
    ser = Series([2, 3], index=[True, False])
    assert is_bool_dtype(ser.index)
    assert ser.index.dtype == bool
    result = ser.drop(True)
    expected = Series([3], index=[False])
    tm.assert_series_equal(result, expected)

