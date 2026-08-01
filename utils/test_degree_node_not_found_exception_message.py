
def test_degree_node_not_found_exception_message():
    """See gh-7740"""
    G = nx.path_graph(5)
    with pytest.raises(nx.NetworkXError, match="Node.*is not in the graph"):
        G.degree(100)

