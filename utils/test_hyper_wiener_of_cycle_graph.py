
def test_hyper_wiener_of_cycle_graph():
    G = nx.cycle_graph(4)
    assert nx.hyper_wiener_index(G) == 20.0

