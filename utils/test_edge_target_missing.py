
def test_edge_target_missing():
    with pytest.raises(nx.NodeNotFound):
        G = nx.Graph()
        nx.add_path(G, [1, 2, 3])
        list(nx.all_simple_edge_paths(nx.MultiGraph(G), 1, 4))

