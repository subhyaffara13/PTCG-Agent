
def test_inplace_arithmetic_series():
    ser = Series([1, 2, 3])
    ser_orig = ser.copy()
    data = get_array(ser)
    ser *= 2
    # https://github.com/pandas-dev/pandas/pull/55745
    # changed to NOT update inplace because there is no benefit (actual
    # operation already done non-inplace). This was only for the optics
    # of updating the backing array inplace, but we no longer want to make
    # that guarantee
    assert not np.shares_memory(get_array(ser), data)
    tm.assert_numpy_array_equal(data, get_array(ser_orig))

