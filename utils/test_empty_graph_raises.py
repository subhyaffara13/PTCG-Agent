
def test_empty_graph_raises(f):
    G = nx.Graph()
    with pytest.raises(nx.NetworkXPointlessConcept, match="Graph has no nodes"):
        f(G)


def test_empty_graph_raises(f):
    G = nx.Graph()
    with pytest.raises(nx.NetworkXPointlessConcept, match="Connectivity is undefined"):
        f(G)

