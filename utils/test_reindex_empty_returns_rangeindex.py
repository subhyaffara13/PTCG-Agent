
def test_reindex_empty_returns_rangeindex():
    ri = RangeIndex(0, 10, 2, name="foo")
    result, result_indexer = ri.reindex([])
    expected = RangeIndex(0, 0, 2, name="foo")
    tm.assert_index_equal(result, expected, exact=True)

    expected_indexer = np.array([], dtype=np.intp)
    tm.assert_numpy_array_equal(result_indexer, expected_indexer)

