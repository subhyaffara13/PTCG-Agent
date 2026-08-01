
def test_raises_node_not_in_G():
    """Check that `tree_broadcast_time` properly raises for invalid nodes."""
    G = nx.path_graph(5)
    with pytest.raises(nx.NodeNotFound, match=r"node.*not in G"):
        nx.tree_broadcast_time(G, node=10)

