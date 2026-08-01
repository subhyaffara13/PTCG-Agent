
def test_where_mask_noop(dtype, func):
    ser = Series([1, 2, 3], dtype=dtype)
    ser_orig = ser.copy()

    result = func(ser)
    assert np.shares_memory(get_array(ser), get_array(result))
    assert result.index is not ser.index

    result.iloc[0] = 10
    assert not np.shares_memory(get_array(ser), get_array(result))
    tm.assert_series_equal(ser, ser_orig)

