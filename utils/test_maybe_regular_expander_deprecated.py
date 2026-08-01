
def test_maybe_regular_expander_deprecated():
    pytest.importorskip("numpy")
    d, n = 2, 7
    with pytest.deprecated_call():
        G = nx.maybe_regular_expander(n, d, seed=1729)

    assert len(G) == n, "Should have n nodes"
    assert len(G.edges) == n * d / 2, "Should have n*d/2 edges"
    assert nx.is_k_regular(G, d), "Should be d-regular"

