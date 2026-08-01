
def test_series_values_ea_dtypes(request, method):
    ser = Series([1, 2, 3], dtype="Int64")
    ser_orig = ser.copy()

    arr = method(ser)

    if request.node.callspec.id in ("values", "array"):
        # https://github.com/pandas-dev/pandas/issues/63099
        # .array/values for now does not return a read-only view
        assert arr.flags.writeable is True
        # updating the array updates the series
        arr[0] = 0
        assert ser.iloc[0] == 0
        return

    # conversion to ndarray gives a view but is read-only
    assert np.shares_memory(arr, get_array(ser))
    assert arr.flags.writeable is False

    # mutating series through arr therefore doesn't work
    with pytest.raises(ValueError, match="read-only"):
        arr[0] = 0
    tm.assert_series_equal(ser, ser_orig)

    # mutating the series itself still works
    ser.iloc[0] = 0
    assert ser.values[0] == 0

