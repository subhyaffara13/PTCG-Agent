
def test_tz_convert_localize(func, tz):
    # GH 49473
    ser = Series(
        [1, 2], index=date_range(start="2014-08-01 09:00", freq="h", periods=2, tz=tz)
    )
    ser_orig = ser.copy()
    ser2 = getattr(ser, func)("US/Central")
    assert np.shares_memory(ser.values, ser2.values)

    # mutating ser triggers a copy-on-write for the column / block
    ser2.iloc[0] = 0
    assert not np.shares_memory(ser2.values, ser.values)
    tm.assert_series_equal(ser, ser_orig)

