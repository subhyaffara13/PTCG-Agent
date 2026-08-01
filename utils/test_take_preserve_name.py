
def test_take_preserve_name(idx):
    taken = idx.take([3, 0, 1])
    assert taken.names == idx.names

