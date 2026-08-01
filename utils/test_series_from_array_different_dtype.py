
def test_series_from_array_different_dtype(copy):
    arr = np.array([1, 2, 3], dtype="int64")
    ser = Series(arr, dtype="int32", copy=copy)
    assert not np.shares_memory(get_array(ser), arr)

