
def test_empty_graph():
    G = nx.Graph()
    nx.draw(G)


def test_empty_graph():
    G = nx.empty_graph(1)
    with pytest.raises(nx.NetworkXError, match=".*not applicable to empty graphs"):
        nx.non_randomness(G)


def test_empty_graph():
    G = nx.Graph()
    G.add_nodes_from(range(5))
    expected = [{0}, {1}, {2}, {3}, {4}]
    assert nx.community.leiden_communities(G) == expected


def test_empty_graph():
    G = nx.Graph()
    G.add_nodes_from(range(5))
    expected = [{0}, {1}, {2}, {3}, {4}]
    assert nx.community.louvain_communities(G) == expected

