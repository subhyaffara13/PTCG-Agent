
def test_greedy_plus_plus_edgeless_cornercase(iterations):
    G = nx.Graph()
    assert approx.densest_subgraph(G, iterations=iterations, method="greedy++") == (
        0,
        set(),
    )
    G.add_nodes_from(range(4))
    assert approx.densest_subgraph(G, iterations=iterations, method="greedy++") == (
        0,
        set(),
    )

