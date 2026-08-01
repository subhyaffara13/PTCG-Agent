
def test_hyper_wiener_of_weighted_graph():
    G = nx.path_graph(3)
    G.edges[0, 1]["weight"] = 2
    assert nx.hyper_wiener_index(G, weight="weight") == 20.0

