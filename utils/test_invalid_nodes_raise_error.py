
def test_invalid_nodes_raise_error(asia_graph):
    """
    Test that graphs that have invalid nodes passed in raise errors.
    """
    # Check both set and node arguments
    with pytest.raises(nx.NodeNotFound):
        nx.is_d_separator(asia_graph, {0}, {1}, {2})
    with pytest.raises(nx.NodeNotFound):
        nx.is_d_separator(asia_graph, 0, 1, 2)
    with pytest.raises(nx.NodeNotFound):
        nx.is_minimal_d_separator(asia_graph, {0}, {1}, {2})
    with pytest.raises(nx.NodeNotFound):
        nx.is_minimal_d_separator(asia_graph, 0, 1, 2)
    with pytest.raises(nx.NodeNotFound):
        nx.find_minimal_d_separator(asia_graph, {0}, {1})
    with pytest.raises(nx.NodeNotFound):
        nx.find_minimal_d_separator(asia_graph, 0, 1)

