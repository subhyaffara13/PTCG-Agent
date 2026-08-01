
def test_neg_returns_rangeindex():
    ri = RangeIndex(2, name="foo")
    result = -ri
    expected = RangeIndex(0, -2, -1, name="foo")
    tm.assert_index_equal(result, expected, exact=True)

    ri = RangeIndex(-2, 2, name="foo")
    result = -ri
    expected = RangeIndex(2, -2, -1, name="foo")
    tm.assert_index_equal(result, expected, exact=True)

