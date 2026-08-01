
def test_constructor_copy_input_timedelta_ndarray_default():
    # GH 63388
    arr = np.array([1, 2], dtype="timedelta64[ns]")
    idx = TimedeltaIndex(arr)
    assert not np.shares_memory(arr, get_array(idx))

