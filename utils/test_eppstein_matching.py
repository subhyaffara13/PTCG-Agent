
def test_eppstein_matching():
    """Test in accordance to issue #1927"""
    G = nx.Graph()
    G.add_nodes_from(["a", 2, 3, 4], bipartite=0)
    G.add_nodes_from([1, "b", "c"], bipartite=1)
    G.add_edges_from([("a", 1), ("a", "b"), (2, "b"), (2, "c"), (3, "c"), (4, 1)])
    matching = eppstein_matching(G)
    assert len(matching) == len(maximum_matching(G))
    assert all(x in set(matching.keys()) for x in set(matching.values()))

