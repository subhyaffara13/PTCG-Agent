
def test_getitem_unordered_dup():
    obj = Series(range(5), index=["c", "a", "a", "b", "b"])
    assert is_scalar(obj["c"])
    assert obj["c"] == 0

