
def test_example_1_detail_3_and_4():
    G = graph_example_1()
    result = k_components(G)
    # In this example graph there are 8 3-components, 4 with 15 nodes
    # and 4 with 5 nodes.
    assert len(result[3]) == 8
    assert len([c for c in result[3] if len(c) == 15]) == 4
    assert len([c for c in result[3] if len(c) == 5]) == 4
    # There are also 8 4-components all with 5 nodes.
    assert len(result[4]) == 8
    assert all(len(c) == 5 for c in result[4])
    # Finally check that the k-components detected have actually node
    # connectivity >= k.
    for k, components in result.items():
        if k < 3:
            continue
        for component in components:
            K = nx.node_connectivity(G.subgraph(component))
            assert K >= k

