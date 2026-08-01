
def test_non_connected():
    G = nx.Graph([(1, 2)])
    G.add_node(3)
    with pytest.raises(nx.NetworkXException, match="Non connected"):
        nx.non_randomness(G)


def test_non_connected():
    with pytest.raises(nx.NetworkXException):
        G = nx.Graph()
        G.add_node(0)
        G.add_node(1)
        nx.second_order_centrality(G)

