import copy

def test_contracted_nodes_multigraph(store_contraction_as, copy, selfloops):
    """Tests that using a MultiGraph creates multiple edges. `store_contraction_as`
    has no effect for multigraphs."""
    G = nx.path_graph(3, create_using=nx.MultiGraph)
    G.add_edges_from([(0, 1), (0, 0), (0, 2)])
    actual = nx.contracted_nodes(
        G,
        0,
        2,
        copy=copy,
        self_loops=selfloops,
        store_contraction_as=store_contraction_as,
    )
    # Two (0, 1) edges from G, another from the contraction of edge (1, 2)
    expected = nx.MultiGraph([(0, 1), (0, 1), (0, 1), (0, 0)])
    # One (0, 0) edge from G, another from the contraction of edge (0, 2), but
    # only if `selfloops` is True
    if selfloops:
        expected.add_edge(0, 0)

    assert edges_equal(actual.edges, expected.edges)
    if not copy:
        assert actual is G

