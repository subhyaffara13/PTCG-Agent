
def test_where_mask(dtype, func):
    ser = Series([1, 2, 3], dtype=dtype)
    ser_orig = ser.copy()

    result = func(ser)

    assert not np.shares_memory(get_array(ser), get_array(result))
    assert result.index is not ser.index
    tm.assert_series_equal(ser, ser_orig)

