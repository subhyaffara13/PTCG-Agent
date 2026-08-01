
def test_getitem_boolmask_returns_rangeindex():
    ri = RangeIndex(3, name="foo")
    result = ri[[False, True, True]]
    expected = RangeIndex(1, 3, name="foo")
    tm.assert_index_equal(result, expected, exact=True)

    result = ri[[True, False, True]]
    expected = RangeIndex(0, 3, 2, name="foo")
    tm.assert_index_equal(result, expected, exact=True)

