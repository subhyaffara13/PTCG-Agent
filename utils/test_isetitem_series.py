
def test_isetitem_series(dtype):
    df = DataFrame({"a": [1, 2, 3], "b": np.array([4, 5, 6], dtype=dtype)})
    ser = Series([7, 8, 9])
    ser_orig = ser.copy()
    df.isetitem(0, ser)

    assert np.shares_memory(get_array(df, "a"), get_array(ser))
    assert not df._mgr._has_no_reference(0)

    # mutating dataframe doesn't update series
    df.loc[0, "a"] = 0
    tm.assert_series_equal(ser, ser_orig)

    # mutating series doesn't update dataframe
    df = DataFrame({"a": [1, 2, 3], "b": np.array([4, 5, 6], dtype=dtype)})
    ser = Series([7, 8, 9])
    df.isetitem(0, ser)

    ser.loc[0] = 0
    expected = DataFrame({"a": [7, 8, 9], "b": np.array([4, 5, 6], dtype=dtype)})
    tm.assert_frame_equal(df, expected)

