
def test_reindex_1_value_returns_rangeindex():
    ri = RangeIndex(0, 10, 2, name="foo")
    result, result_indexer = ri.reindex([2])
    expected = RangeIndex(2, 4, 2, name="foo")
    tm.assert_index_equal(result, expected, exact=True)

    expected_indexer = np.array([1], dtype=np.intp)
    tm.assert_numpy_array_equal(result_indexer, expected_indexer)

