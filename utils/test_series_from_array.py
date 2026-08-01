
def test_series_from_array(idx, dtype, arr):
    ser = Series(arr, dtype=dtype, index=idx)
    ser_orig = ser.copy()
    data = getattr(arr, "_data", arr)
    assert not np.shares_memory(get_array(ser), data)

    arr[0] = 100
    tm.assert_series_equal(ser, ser_orig)

    # if the user explicitly passes copy=False, we get an actual view
    # not protected by CoW
    ser = Series(arr, dtype=dtype, index=idx, copy=False)
    assert np.shares_memory(get_array(ser), data)
    arr[0] = 50
    assert ser.iloc[0] == 50

