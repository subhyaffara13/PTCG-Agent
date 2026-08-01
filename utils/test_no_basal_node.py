
def test_no_basal_node():
    G = nx.DiGraph([(1, 2), (2, 3), (3, 1)])  # No basal node, should raise an error
    with pytest.raises(nx.NetworkXError, match="no basal node"):
        nx.trophic_levels(G)
    G.add_node(4)  # add basal node, but not connected
    with pytest.raises(nx.NetworkXError, match="every node .* path from a basal node"):
        nx.trophic_levels(G)

