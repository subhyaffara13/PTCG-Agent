
def test_series_to_numpy():
    ser = Series([1, 2, 3], name="name")
    ser_orig = ser.copy()

    # default: copy=False, no dtype or NAs
    arr = ser.to_numpy()
    # to_numpy still gives a view but is read-only
    assert np.shares_memory(arr, get_array(ser, "name"))
    assert arr.flags.writeable is False

    # mutating series through arr therefore doesn't work
    with pytest.raises(ValueError, match="read-only"):
        arr[0] = 0
    tm.assert_series_equal(ser, ser_orig)

    # mutating the series itself still works
    ser.iloc[0] = 0
    assert ser.values[0] == 0

    # specify copy=True gives a writeable array
    ser = Series([1, 2, 3], name="name")
    arr = ser.to_numpy(copy=True)
    assert not np.shares_memory(arr, get_array(ser, "name"))
    assert arr.flags.writeable is True

    # specifying a dtype that already causes a copy also gives a writeable array
    ser = Series([1, 2, 3], name="name")
    arr = ser.to_numpy(dtype="float64")
    assert not np.shares_memory(arr, get_array(ser, "name"))
    assert arr.flags.writeable is True

