
def test_pos_returns_rangeindex():
    ri = RangeIndex(2, name="foo")
    expected = ri.copy()
    result = +ri
    tm.assert_index_equal(result, expected, exact=True)

