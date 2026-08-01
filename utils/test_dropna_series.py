
def test_dropna_series(val):
    ser = Series([1, val, 4])
    ser_orig = ser.copy()
    ser2 = ser.dropna()
    assert np.shares_memory(ser2.values, ser.values)

    ser2.iloc[0] = 0
    assert not np.shares_memory(ser2.values, ser.values)
    tm.assert_series_equal(ser, ser_orig)

