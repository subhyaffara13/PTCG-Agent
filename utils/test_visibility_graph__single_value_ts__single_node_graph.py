
def test_visibility_graph__single_value_ts__single_node_graph():
    node_graph = nx.visibility_graph([10])  # So Lonely
    assert node_graph.number_of_nodes() == 1
    assert node_graph.number_of_edges() == 0

