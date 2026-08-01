
def test_reindex_returns_rangeindex():
    ri = RangeIndex(2, name="foo")
    result, result_indexer = ri.reindex([1, 2, 3])
    expected = RangeIndex(1, 4, name="foo")
    tm.assert_index_equal(result, expected, exact=True)

    expected_indexer = np.array([1, -1, -1], dtype=np.intp)
    tm.assert_numpy_array_equal(result_indexer, expected_indexer)

