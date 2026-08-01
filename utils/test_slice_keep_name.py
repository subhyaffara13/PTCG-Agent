
def test_slice_keep_name():
    x = MultiIndex.from_tuples([("a", "b"), (1, 2), ("c", "d")], names=["x", "y"])
    assert x[1:].names == x.names

