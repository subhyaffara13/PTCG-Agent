
def test_directed_node_contraction(store_contraction_as, copy, selfloops):
    """Tests for node contraction in a directed graph."""
    G = nx.DiGraph(nx.cycle_graph(4))
    actual = nx.contracted_nodes(
        G,
        0,
        1,
        copy=copy,
        self_loops=selfloops,
        store_contraction_as=store_contraction_as,
    )

    expected = nx.DiGraph(nx.cycle_graph(3))
    if selfloops:
        expected.add_edge(0, 0)

    assert nx.is_isomorphic(actual, expected)

    if not copy:
        assert actual is G
    # Test contracted node attributes
    if store_contraction_as is not None:
        assert actual.nodes[0][store_contraction_as] == {1: {}}
    else:
        assert actual.nodes[0] == {}
    # Test contracted edge attributes (only relevant if self loops is enabled)
    if selfloops and store_contraction_as:
        assert actual.edges[(0, 0)][store_contraction_as] == {(1, 0): {}}
    else:
        assert all(d == {} for _, _, d in actual.edges(data=True))

