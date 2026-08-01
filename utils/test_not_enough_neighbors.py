
def test_not_enough_neighbors():
    with pytest.raises(NetworkXError):
        G = complete_bipartite_graph(1, 2)
        node_redundancy(G)

