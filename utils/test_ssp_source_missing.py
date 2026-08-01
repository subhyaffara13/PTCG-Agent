
def test_ssp_source_missing():
    with pytest.raises(nx.NodeNotFound):
        G = nx.Graph()
        nx.add_path(G, [1, 2, 3])
        list(nx.shortest_simple_paths(G, 0, 3))

