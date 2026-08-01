
def test_getitem_boolmask_all_true():
    ri = RangeIndex(3, name="foo")
    expected = ri.copy()
    result = ri[[True] * 3]
    tm.assert_index_equal(result, expected, exact=True)

