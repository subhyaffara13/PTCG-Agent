
def test_constructor_copy_input_datetime_ndarray_default():
    # GH 63388
    arr = np.array(["2020-01-01", "2020-01-02"], dtype="datetime64[ns]")
    idx = DatetimeIndex(arr)
    assert not np.shares_memory(arr, get_array(idx))

