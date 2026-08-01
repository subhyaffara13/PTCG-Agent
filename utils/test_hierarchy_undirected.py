
def test_hierarchy_undirected():
    G = nx.cycle_graph(5)
    pytest.raises(nx.NetworkXError, nx.flow_hierarchy, G)

