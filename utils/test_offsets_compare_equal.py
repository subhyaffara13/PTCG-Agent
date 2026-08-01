
def test_offsets_compare_equal(_offset):
    # root cause of GH#456: __ne__ was not implemented
    offset1 = _offset()
    offset2 = _offset()
    assert not offset1 != offset2
    assert offset1 == offset2

