
def test_multigraph():
    G = nx.MultiGraph()
    G.add_edge(1, 2, key="first")
    G.add_edge(1, 2, key="second", color="blue")
    H = cytoscape_graph(cytoscape_data(G))
    assert nx.is_isomorphic(G, H)
    assert H[1][2]["second"]["color"] == "blue"


def test_multigraph():
    G = nx.cycle_graph(4)
    M = nx.MultiGraph(G.edges())
    M.add_edges_from(G.edges())
    M.remove_edge(1, 2)
    for labels in permutations(range(4)):
        mapping = dict(zip(M, labels))
        A, B = kernighan_lin_bisection(nx.relabel_nodes(M, mapping), seed=0)
        assert_partition_equal(
            [A, B], [{mapping[0], mapping[1]}, {mapping[2], mapping[3]}]
        )


def test_multigraph():
    G = nx.karate_club_graph()
    H = nx.MultiGraph(G)
    G.add_edge(0, 1, weight=10)
    H.add_edge(0, 1, weight=9)
    G.add_edge(0, 9, foo=20)
    H.add_edge(0, 9, foo=20)

    partition1 = nx.community.louvain_communities(G, seed=1234)
    partition2 = nx.community.louvain_communities(H, seed=1234)
    partition3 = nx.community.louvain_communities(H, weight="foo", seed=1234)

    assert partition1 == partition2 != partition3

