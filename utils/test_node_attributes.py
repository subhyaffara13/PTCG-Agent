
def test_node_attributes(store_contraction_as, copy, selfloops):
    """Tests that node contraction preserves node attributes."""
    G = nx.cycle_graph(4)
    # Add some data to the two nodes being contracted.
    G.nodes[0]["foo"] = "bar"
    G.nodes[1]["baz"] = "xyzzy"
    actual = nx.contracted_nodes(
        G,
        0,
        1,
        copy=copy,
        self_loops=selfloops,
        store_contraction_as=store_contraction_as,
    )
    # We expect that contracting the nodes 0 and 1 in C_4 yields K_3, but
    # with nodes labeled 0, 2, and 3.
    expected = nx.complete_graph(3)
    expected = nx.relabel_nodes(expected, {1: 2, 2: 3})
    expected.nodes[0]["foo"] = "bar"
    # ... and a self-loop (0, 0), if self_loops=True
    if selfloops:
        expected.add_edge(0, 0)

    if store_contraction_as:
        cdict = {1: {"baz": "xyzzy"}}
        expected.nodes[0].update({"foo": "bar", store_contraction_as: cdict})

    assert nx.is_isomorphic(actual, expected)
    assert actual.nodes(data=True) == expected.nodes(data=True)
    if not copy:
        assert actual is G

