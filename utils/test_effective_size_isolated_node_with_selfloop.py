
def test_effective_size_isolated_node_with_selfloop(graph, nodes):
    """Behavior consistent with isolated node without self-loop. See gh-6916"""
    G = graph([(0, 0)])  # Single node with one self-edge
    assert math.isnan(nx.effective_size(G, nodes=nodes)[0])

