
def test_ssp_source_missing2():
    with pytest.raises(nx.NetworkXNoPath):
        G = nx.Graph()
        nx.add_path(G, [0, 1, 2])
        nx.add_path(G, [3, 4, 5])
        list(nx.shortest_simple_paths(G, 0, 3))

