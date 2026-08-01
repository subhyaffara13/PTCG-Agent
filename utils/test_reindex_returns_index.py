
def test_reindex_returns_index():
    ri = RangeIndex(4, name="foo")
    result, result_indexer = ri.reindex([0, 1, 3])
    expected = Index([0, 1, 3], name="foo")
    tm.assert_index_equal(result, expected, exact=True)

    expected_indexer = np.array([0, 1, 3], dtype=np.intp)
    tm.assert_numpy_array_equal(result_indexer, expected_indexer)

