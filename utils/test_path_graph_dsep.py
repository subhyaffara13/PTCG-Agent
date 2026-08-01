
def test_path_graph_dsep(path_graph):
    """Example-based test of d-separation for path_graph."""
    assert nx.is_d_separator(path_graph, {0}, {2}, {1})
    assert not nx.is_d_separator(path_graph, {0}, {2}, set())

