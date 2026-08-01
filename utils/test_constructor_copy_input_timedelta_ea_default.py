
def test_constructor_copy_input_timedelta_ea_default():
    # GH 63388
    arr = array([1, 2], dtype="timedelta64[ns]")
    idx = TimedeltaIndex(arr)
    assert not tm.shares_memory(arr, idx.array)

