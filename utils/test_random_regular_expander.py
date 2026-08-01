
def test_random_regular_expander(d, n):
    pytest.importorskip("numpy")
    pytest.importorskip("scipy")
    G = nx.random_regular_expander_graph(n, d, seed=1729)

    assert len(G) == n, "Should have n nodes"
    assert len(G.edges) == n * d / 2, "Should have n*d/2 edges"
    assert nx.is_k_regular(G, d), "Should be d-regular"
    assert nx.is_regular_expander(G), "Should be a regular expander"

