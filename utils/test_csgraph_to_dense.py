
def test_csgraph_to_dense():
    np.random.seed(1234)
    G = np.random.random((10, 10))
    nulls = (G < 0.8)
    G[nulls] = np.inf

    G_csr = csgraph_from_dense(G)

    for null_value in [0, 10, -np.inf, np.inf]:
        G[nulls] = null_value
        assert_array_almost_equal(G, csgraph_to_dense(G_csr, null_value))

