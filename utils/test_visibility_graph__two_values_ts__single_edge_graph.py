
def test_visibility_graph__two_values_ts__single_edge_graph():
    edge_graph = nx.visibility_graph([10, 20])  # Two of Us
    assert list(edge_graph.edges) == [(0, 1)]

