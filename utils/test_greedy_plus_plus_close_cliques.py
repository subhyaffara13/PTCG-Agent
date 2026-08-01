
def test_greedy_plus_plus_close_cliques():
    G, best_density, densest_set = close_cliques_example()
    # NOTE: iterations=185 fails to ID the densest subgraph
    greedy_pp, S_pp = approx.densest_subgraph(G, iterations=186, method="greedy++")

    assert greedy_pp == pytest.approx(best_density)
    assert S_pp == densest_set

