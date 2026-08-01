
def test_v_structures_raise():
    G = nx.Graph()
    with pytest.raises(nx.NetworkXNotImplemented, match="for undirected type"):
        nx.dag.v_structures(G)

