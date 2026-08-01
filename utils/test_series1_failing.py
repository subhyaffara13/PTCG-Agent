
def test_series1_failing():
    assert x.nseries(x, 0, 0) == O(1, x)
    assert x.nseries(x, 0, 1) == O(x, x)

