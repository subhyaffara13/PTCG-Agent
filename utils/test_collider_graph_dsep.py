
def test_collider_graph_dsep(collider_graph):
    """Example-based test of d-separation for collider_graph."""
    assert nx.is_d_separator(collider_graph, {0}, {1}, set())
    assert not nx.is_d_separator(collider_graph, {0}, {1}, {2})

