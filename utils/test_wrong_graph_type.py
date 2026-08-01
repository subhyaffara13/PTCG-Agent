
def test_wrong_graph_type(fn, graph_type):
    G = graph_type()
    with pytest.raises(nx.NetworkXNotImplemented):
        fn(G)

