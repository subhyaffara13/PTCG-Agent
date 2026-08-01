
def test_same_node_is_reachable():
    """Tests that a node is always reachable from it."""
    # G is an arbitrary tournament on ten nodes.
    G = DiGraph(sorted(p) for p in combinations(range(10), 2))
    assert all(is_reachable(G, v, v) for v in G)

