
def test_int64_indices_directed():
    # See https://github.com/scipy/scipy/issues/18716
    g = csr_array(([1], np.array([[0], [1]], dtype=np.int64)), shape=(2, 2))
    assert g.indices.dtype == np.int64
    n, labels = csgraph.connected_components(g, directed=True,
                                             connection='strong')
    assert n == 2
    assert_array_almost_equal(labels, [1, 0])

