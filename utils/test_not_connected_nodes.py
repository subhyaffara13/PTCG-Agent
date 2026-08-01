
def test_not_connected_nodes():
    with pytest.raises(nx.NetworkXNoPath):
        G = nx.Graph()
        nx.add_path(G, [1, 2, 3])
        nx.add_path(G, [4, 5])
        list(nx.node_disjoint_paths(G, 1, 5))

