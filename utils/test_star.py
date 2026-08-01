
def test_star():
    G = nx.star_graph(3)
    _check_augmentations(G)

    G = nx.star_graph(5)
    _check_augmentations(G)

    G = nx.star_graph(10)
    _check_augmentations(G)


def test_star(n, iterations, method):
    if method == "fista":
        pytest.importorskip("numpy")

    G = nx.star_graph(n)
    # The densest subgraph of a star network is the entire graph.
    # The peeling algorithm would peel all the vertices with degree 1,
    # and so should discover the densest subgraph in one iteration!
    d, S = approx.densest_subgraph(G, iterations=iterations, method=method)

    assert d == pytest.approx(G.number_of_edges() / G.number_of_nodes())
    assert S == set(G)  # The entire graph!

