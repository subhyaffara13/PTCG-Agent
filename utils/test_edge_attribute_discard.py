
def test_edge_attribute_discard():
    # Test that edge attributes are discarded if we do not specify to keep them
    G = nx.Graph()

    edgelist = [
        (0, 1, [("weight", 5), ("otherattr", 1), ("otherattr2", 3)]),
        (0, 2, [("weight", 5), ("otherattr", 2), ("otherattr2", 2)]),
        (1, 2, [("weight", 6), ("otherattr", 3), ("otherattr2", 1)]),
    ]
    G.add_edges_from(edgelist)

    B = branchings.maximum_branching(G, preserve_attrs=False)

    edge_dict = B[0][1]
    with pytest.raises(KeyError):
        _ = edge_dict["otherattr"]

