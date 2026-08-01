
def test_outer_join_indexer():
    a = np.array([1, 2, 3, 4, 5], dtype=np.int64)
    b = np.array([0, 3, 5, 7, 9], dtype=np.int64)

    index, ares, bres = libjoin.outer_join_indexer(a, b)

    index_exp = np.array([0, 1, 2, 3, 4, 5, 7, 9], dtype=np.int64)
    tm.assert_almost_equal(index, index_exp)

    aexp = np.array([-1, 0, 1, 2, 3, 4, -1, -1], dtype=np.intp)
    bexp = np.array([0, -1, -1, 1, -1, 2, 3, 4], dtype=np.intp)
    tm.assert_almost_equal(ares, aexp)
    tm.assert_almost_equal(bres, bexp)

    a = np.array([5], dtype=np.int64)
    b = np.array([5], dtype=np.int64)

    index, ares, bres = libjoin.outer_join_indexer(a, b)
    tm.assert_numpy_array_equal(index, np.array([5], dtype=np.int64))
    tm.assert_numpy_array_equal(ares, np.array([0], dtype=np.intp))
    tm.assert_numpy_array_equal(bres, np.array([0], dtype=np.intp))

