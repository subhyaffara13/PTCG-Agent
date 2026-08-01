
def test_api_mi_raises():
    # GH 23679
    mi = MultiIndex.from_arrays([["a", "b", "c"]])
    msg = "Can only use .str accessor with Index, not MultiIndex"
    with pytest.raises(AttributeError, match=msg):
        mi.str
    assert not hasattr(mi, "str")

