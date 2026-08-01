
def test_greedy_plus_plus_bipartite_and_clique():
    G, best_density, best_subgraph, correct_one_iter_density = (
        bipartite_and_clique_example()
    )
    one_round_density, S_one = approx.densest_subgraph(
        G, iterations=1, method="greedy++"
    )
    assert one_round_density == pytest.approx(correct_one_iter_density)
    assert S_one == set(G.nodes)

    ten_round_density, S_ten = approx.densest_subgraph(
        G, iterations=10, method="greedy++"
    )
    assert ten_round_density == pytest.approx(best_density)
    assert S_ten == best_subgraph

