
def test_undirected_graphs_are_not_supported():
    """
    Test that undirected graphs are not supported.

    d-separation and its related algorithms do not apply in
    the case of undirected graphs.
    """
    g = nx.path_graph(3, nx.Graph)
    with pytest.raises(nx.NetworkXNotImplemented):
        nx.is_d_separator(g, {0}, {1}, {2})
    with pytest.raises(nx.NetworkXNotImplemented):
        nx.is_minimal_d_separator(g, {0}, {1}, {2})
    with pytest.raises(nx.NetworkXNotImplemented):
        nx.find_minimal_d_separator(g, {0}, {1})

