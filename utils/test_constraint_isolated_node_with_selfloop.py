
def test_constraint_isolated_node_with_selfloop(graph):
    """Behavior consistent with isolated node without self-loop. See gh-6916"""
    G = graph([(0, 0)])  # Single node with one self-edge
    assert math.isnan(nx.constraint(G)[0])

