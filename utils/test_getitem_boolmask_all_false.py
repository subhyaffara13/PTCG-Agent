
def test_getitem_boolmask_all_false():
    ri = RangeIndex(3, name="foo")
    result = ri[[False] * 3]
    expected = RangeIndex(0, name="foo")
    tm.assert_index_equal(result, expected, exact=True)

