
def test_series_from_temporary_index_readonly_data():
    # GH 63370
    arr = np.array([0, 1], dtype=np.dtype(np.int8))
    arr.flags.writeable = False
    ser = Series(Index(arr))
    assert not np.shares_memory(arr, get_array(ser))
    assert ser._mgr._has_no_reference(0)
    ser[[False, True]] = np.array([0, 2], dtype=np.dtype(np.int8))
    expected = Series([0, 2], dtype=np.dtype(np.int8))
    tm.assert_series_equal(ser, expected)

