
def test_colliders_raise():
    G = nx.Graph()
    with pytest.raises(nx.NetworkXNotImplemented, match="for undirected type"):
        nx.dag.colliders(G)

