
def test_to_networkx_graph_non_edgelist():
    invalid_edgelist = [1, 2, 3]
    with pytest.raises(nx.NetworkXError, match="Input is not a valid edge list"):
        nx.to_networkx_graph(invalid_edgelist)

