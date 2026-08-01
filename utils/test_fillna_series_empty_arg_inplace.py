
def test_fillna_series_empty_arg_inplace():
    ser = Series([1, np.nan, 2])
    arr = get_array(ser)
    ser.fillna({}, inplace=True)

    assert np.shares_memory(get_array(ser), arr)
    assert ser._mgr._has_no_reference(0)

