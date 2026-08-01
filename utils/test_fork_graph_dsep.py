
def test_fork_graph_dsep(fork_graph):
    """Example-based test of d-separation for fork_graph."""
    assert nx.is_d_separator(fork_graph, {1}, {2}, {0})
    assert not nx.is_d_separator(fork_graph, {1}, {2}, set())

