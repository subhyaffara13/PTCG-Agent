
def test_torrents_and_ferraro_graph():
    G = torrents_and_ferraro_graph()
    result = nx.k_components(G)
    _check_connectivity(G, result)

    # In this example graph there are 8 3-components, 4 with 15 nodes
    # and 4 with 5 nodes.
    assert len(result[3]) == 8
    assert len([c for c in result[3] if len(c) == 15]) == 4
    assert len([c for c in result[3] if len(c) == 5]) == 4
    # There are also 8 4-components all with 5 nodes.
    assert len(result[4]) == 8
    assert all(len(c) == 5 for c in result[4])


def test_torrents_and_ferraro_graph():
    G = torrents_and_ferraro_graph()
    _check_separating_sets(G)


def test_torrents_and_ferraro_graph():
    G = torrents_and_ferraro_graph()
    _check_connectivity(G)

