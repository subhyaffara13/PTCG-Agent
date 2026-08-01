
def test_fista_close_cliques():
    pytest.importorskip("numpy")
    G, best_density, best_set = close_cliques_example()
    # NOTE: iterations=12 fails to ID the densest subgraph
    density, dense_set = approx.densest_subgraph(G, iterations=13, method="fista")

    assert density == pytest.approx(best_density)
    assert dense_set == best_set

