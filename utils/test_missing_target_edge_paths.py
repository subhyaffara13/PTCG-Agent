
def test_missing_target_edge_paths():
    with pytest.raises(nx.NetworkXError):
        G = nx.path_graph(4)
        list(nx.edge_disjoint_paths(G, 1, 10))

