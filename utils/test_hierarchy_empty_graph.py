
def test_hierarchy_empty_graph(n):
    G = nx.empty_graph(n, create_using=nx.DiGraph)
    with pytest.raises(nx.NetworkXError, match=".*not applicable to empty graphs"):
        nx.flow_hierarchy(G)

