
def test_append_non_rangeindex_return_rangeindex():
    ri = RangeIndex(1)
    result = ri.append(Index([1]))
    expected = RangeIndex(2)
    tm.assert_index_equal(result, expected, exact=True)

