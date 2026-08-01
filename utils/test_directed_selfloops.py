
def test_directed_selfloops():
    G = nx.DiGraph()
    G.add_nodes_from(range(11))
    G_edges = [
        (0, 2),
        (0, 1),
        (1, 0),
        (2, 1),
        (2, 0),
        (3, 4),
        (4, 3),
        (7, 8),
        (8, 7),
        (9, 10),
        (10, 9),
    ]
    G.add_edges_from(G_edges)
    G_expected_partition = nx.community.louvain_communities(G, seed=123, weight=None)

    G.add_weighted_edges_from([(i, i, i * 1000) for i in range(3)])
    # large self-loop weight impacts partition
    G_partition = nx.community.louvain_communities(G, seed=123, weight="weight")
    assert G_partition != G_expected_partition

    # small self-loop weights aren't enough to impact partition in this graph
    G_partition = nx.community.louvain_communities(G, seed=123, weight=None)
    assert G_partition == G_expected_partition

