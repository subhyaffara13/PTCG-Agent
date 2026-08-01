
def test_isolated_nodes():
    with pytest.raises(nx.NetworkXNoPath):
        G = nx.Graph()
        G.add_node(1)
        nx.add_path(G, [4, 5])
        list(nx.node_disjoint_paths(G, 1, 5))

