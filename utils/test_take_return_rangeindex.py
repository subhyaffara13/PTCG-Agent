
def test_take_return_rangeindex():
    ri = RangeIndex(5, name="foo")
    result = ri.take([])
    expected = RangeIndex(0, name="foo")
    tm.assert_index_equal(result, expected, exact=True)

    result = ri.take([3, 4])
    expected = RangeIndex(3, 5, name="foo")
    tm.assert_index_equal(result, expected, exact=True)

