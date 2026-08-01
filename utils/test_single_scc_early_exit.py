
def test_single_scc_early_exit():
    # Exercises the early-exit check
    rows = [0, 1, 1, 2, 3, 3, 4, 5]
    cols = [1, 2, 5, 3, 1, 4, 0, 2]
    data = np.ones(len(rows), dtype=np.int32)
    g = csr_array((data, (rows, cols)), shape=(6, 6))
    n_components, labels = csgraph.connected_components(
        g, directed=True, connection='strong')
    assert_equal(n_components, 1)
    assert_equal(len(np.unique(labels)), 1)

