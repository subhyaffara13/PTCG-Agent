
def test_slice_can_reorder_not_uniquely_indexed():
    ser = Series(1, index=["a", "a", "b", "b", "c"])
    ser[::-1]  # it works!

