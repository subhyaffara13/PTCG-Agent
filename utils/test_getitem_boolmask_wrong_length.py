
def test_getitem_boolmask_wrong_length():
    ri = RangeIndex(4, name="foo")
    with pytest.raises(IndexError, match="Boolean index has wrong length"):
        ri[[True]]

