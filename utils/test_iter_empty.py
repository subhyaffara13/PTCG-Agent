
def test_iter_empty(temp_hdfstore):
    # GH 12221
    assert list(temp_hdfstore) == []

