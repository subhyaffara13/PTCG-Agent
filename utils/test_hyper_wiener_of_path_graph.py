
def test_hyper_wiener_of_path_graph():
    G = nx.path_graph(4)
    assert nx.hyper_wiener_index(G) == 30.0

