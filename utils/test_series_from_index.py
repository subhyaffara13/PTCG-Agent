
def test_series_from_index(idx):
    ser = Series(idx)
    expected = idx.copy(deep=True)
    assert np.shares_memory(get_array(ser), get_array(idx))
    assert not ser._mgr._has_no_reference(0)
    ser.iloc[0] = ser.iloc[1]
    tm.assert_index_equal(idx, expected)

    # forcing copy=False still gives a CoW shallow copy
    ser = Series(idx, copy=False)
    assert np.shares_memory(get_array(ser), get_array(idx))
    assert not ser._mgr._has_no_reference(0)
    ser.iloc[0] = ser.iloc[1]
    tm.assert_index_equal(idx, expected)

    # forcing copy=True still results in a copy
    ser = Series(idx, copy=True)
    assert not np.shares_memory(get_array(ser), get_array(idx))
    assert ser._mgr._has_no_reference(0)

