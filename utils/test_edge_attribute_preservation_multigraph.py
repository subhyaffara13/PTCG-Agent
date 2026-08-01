
def test_edge_attribute_preservation_multigraph():
    # Test that edge attributes are preserved when finding an optimum graph
    # using the Edmonds class for multigraphs.
    G = nx.MultiGraph()

    edgelist = [
        (0, 1, [("weight", 5), ("otherattr", 1), ("otherattr2", 3)]),
        (0, 2, [("weight", 5), ("otherattr", 2), ("otherattr2", 2)]),
        (1, 2, [("weight", 6), ("otherattr", 3), ("otherattr2", 1)]),
    ]
    G.add_edges_from(edgelist * 2)  # Make sure we have duplicate edge paths

    B = branchings.maximum_branching(G, preserve_attrs=True)

    assert B[0][1][0]["otherattr"] == 1
    assert B[0][1][0]["otherattr2"] == 3

