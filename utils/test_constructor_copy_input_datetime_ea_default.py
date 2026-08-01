
def test_constructor_copy_input_datetime_ea_default():
    # GH 63388
    arr = array(["2020-01-01", "2020-01-02"], dtype="datetime64[ns]")
    idx = DatetimeIndex(arr)
    assert not tm.shares_memory(arr, idx.array)

