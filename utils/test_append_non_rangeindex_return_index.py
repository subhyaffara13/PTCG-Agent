
def test_append_non_rangeindex_return_index():
    ri = RangeIndex(1)
    result = ri.append(Index([1, 3, 4]))
    expected = Index([0, 1, 3, 4])
    tm.assert_index_equal(result, expected, exact=True)

