import copy

def test_series_from_index_different_dtypes(copy):
    idx = Index([1, 2, 3], dtype="int64", copy=copy)
    ser = Series(idx, dtype="int32")
    assert not np.shares_memory(get_array(ser), get_array(idx))
    assert ser._mgr._has_no_reference(0)

