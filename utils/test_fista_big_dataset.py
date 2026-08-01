
def test_fista_big_dataset():
    pytest.importorskip("numpy")
    G, best_density, best_subgraph = close_cliques_example(d=30, D=2000, h=60, k=20)

    # Note: iterations=12 fails to identify densest subgraph
    density, dense_set = approx.densest_subgraph(G, iterations=13, method="fista")

    assert density == pytest.approx(best_density)
    assert dense_set == best_subgraph

