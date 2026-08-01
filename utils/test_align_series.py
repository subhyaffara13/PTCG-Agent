
def test_align_series():
    ser = Series([1, 2])
    ser_orig = ser.copy()
    ser_other = ser.copy()
    ser2, ser_other_result = ser.align(ser_other)

    assert np.shares_memory(ser2.values, ser.values)
    assert np.shares_memory(ser_other_result.values, ser_other.values)
    ser2.iloc[0] = 0
    ser_other_result.iloc[0] = 0
    assert not np.shares_memory(ser2.values, ser.values)
    assert not np.shares_memory(ser_other_result.values, ser_other.values)
    tm.assert_series_equal(ser, ser_orig)
    tm.assert_series_equal(ser_other, ser_orig)

