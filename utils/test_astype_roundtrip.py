
def test_astype_roundtrip(dtype):
    ser = pd.Series(pd.date_range("2000", periods=12, unit="ns"))
    ser[0] = None

    casted = ser.astype(dtype)
    assert is_dtype_equal(casted.dtype, dtype)

    result = casted.astype("datetime64[ns]")
    tm.assert_series_equal(result, ser)

    # GH#38509 same thing for timedelta64
    ser2 = ser - ser.iloc[-1]
    casted2 = ser2.astype(dtype)
    assert is_dtype_equal(casted2.dtype, dtype)

    result2 = casted2.astype(ser2.dtype)
    tm.assert_series_equal(result2, ser2)

