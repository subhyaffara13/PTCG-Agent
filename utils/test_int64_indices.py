
def test_int64_indices(tree_func, directed):
    # See https://github.com/scipy/scipy/issues/18716
    g = csr_array(([1], np.array([[0], [1]], dtype=np.int64)), shape=(2, 2))
    assert g.indices.dtype == np.int64
    tree = tree_func(g, 0, directed=directed)
    assert_array_almost_equal(csgraph_to_dense(tree), [[0, 1], [0, 0]])

