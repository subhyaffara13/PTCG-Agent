
def test_constructor_copy_input_interval_ea_default():
    # GH 63388
    arr = array([Interval(0, 1), Interval(1, 2)])
    idx = IntervalIndex(arr)
    assert not tm.shares_memory(arr, idx.array)

