
def test_not_bipartite():
    with pytest.raises(nx.NetworkXError):
        bipartite.clustering(nx.complete_graph(4))

