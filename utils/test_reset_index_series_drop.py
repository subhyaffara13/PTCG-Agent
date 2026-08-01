
def test_reset_index_series_drop(index):
    ser = Series([1, 2], index=index)
    ser_orig = ser.copy()
    ser2 = ser.reset_index(drop=True)
    assert np.shares_memory(get_array(ser), get_array(ser2))
    assert not ser._mgr._has_no_reference(0)

    ser2.iloc[0] = 100
    tm.assert_series_equal(ser, ser_orig)

