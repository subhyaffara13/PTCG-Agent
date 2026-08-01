
def test_hyper_wiener_of_disconnected_graph():
    G = nx.Graph([(0, 1), (2, 3)])
    assert nx.hyper_wiener_index(G) == float("inf")

