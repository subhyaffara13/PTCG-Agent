
def test_getitem_boolmask_returns_index():
    ri = RangeIndex(4, name="foo")
    result = ri[[True, True, False, True]]
    expected = Index([0, 1, 3], name="foo")
    tm.assert_index_equal(result, expected)

