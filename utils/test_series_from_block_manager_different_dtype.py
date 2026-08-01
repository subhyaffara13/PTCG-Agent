
def test_series_from_block_manager_different_dtype():
    ser = Series([1, 2, 3], dtype="int64")
    msg = "Passing a SingleBlockManager to Series"
    with tm.assert_produces_warning(DeprecationWarning, match=msg):
        ser2 = Series(ser._mgr, dtype="int32")
    assert not np.shares_memory(get_array(ser), get_array(ser2))
    assert ser2._mgr._has_no_reference(0)

