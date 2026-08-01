
def test_multigraph_edge_contraction(edge, store_contraction_as, copy, selfloops):
    """Tests for edge contraction in a multigraph"""
    G = nx.cycle_graph(4, create_using=nx.MultiGraph)
    actual = nx.contracted_edge(
        G,
        edge,
        copy=copy,
        self_loops=selfloops,
        store_contraction_as=store_contraction_as,
    )
    expected = nx.relabel_nodes(
        nx.complete_graph(3, create_using=nx.MultiGraph), {0: 0, 1: 2, 2: 3}
    )
    if selfloops:
        expected.add_edge(0, 0)

    assert edges_equal(actual.edges, expected.edges)
    if not copy:
        assert actual is G

