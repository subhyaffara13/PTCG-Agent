
def test_inplace_arithmetic_series_with_reference():
    ser = Series([1, 2, 3])
    ser_orig = ser.copy()
    view = ser[:]
    ser *= 2
    assert not np.shares_memory(get_array(ser), get_array(view))
    tm.assert_series_equal(ser_orig, view)

