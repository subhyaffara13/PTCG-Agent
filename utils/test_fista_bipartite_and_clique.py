
def test_fista_bipartite_and_clique():
    pytest.importorskip("numpy")
    G, best_density, best_subgraph, _ = bipartite_and_clique_example()

    ten_round_density, S_ten = approx.densest_subgraph(G, iterations=10, method="fista")
    assert ten_round_density == pytest.approx(best_density)
    assert S_ten == best_subgraph

