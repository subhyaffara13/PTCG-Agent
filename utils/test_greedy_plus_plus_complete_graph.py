
def test_greedy_plus_plus_complete_graph(method):
    if method == "fista":
        pytest.importorskip("numpy")

    G = nx.complete_graph(4)
    # The density of a complete graph network is the entire graph: C(4, 2)/4
    # where C(n, 2) is n*(n-1)//2. The peeling algorithm would find
    # the densest subgraph in one iteration!
    d, S = approx.densest_subgraph(G, iterations=1, method=method)

    assert d == pytest.approx(6 / 4)  # The density, 4/5=0.8.
    assert S == {0, 1, 2, 3}  # The entire graph!

