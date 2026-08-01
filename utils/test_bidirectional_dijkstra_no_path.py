
def test_bidirectional_dijkstra_no_path():
    with pytest.raises(nx.NetworkXNoPath):
        G = nx.Graph()
        nx.add_path(G, [1, 2, 3])
        nx.add_path(G, [4, 5, 6])
        _bidirectional_dijkstra(G, 1, 6)

