
def test_invalid_auxiliary():
    G = nx.complete_graph(5)
    pytest.raises(nx.NetworkXError, local_node_connectivity, G, 0, 3, auxiliary=G)


def test_invalid_auxiliary():
    G = nx.complete_graph(5)
    pytest.raises(nx.NetworkXError, minimum_st_node_cut, G, 0, 3, auxiliary=G)


def test_invalid_auxiliary():
    with pytest.raises(nx.NetworkXError):
        G = nx.complete_graph(5)
        list(nx.node_disjoint_paths(G, 0, 3, auxiliary=G))

