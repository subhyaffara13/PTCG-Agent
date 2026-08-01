
def test_bad_mode():
    with pytest.raises(nx.NetworkXError):
        bipartite.clustering(nx.path_graph(4), mode="foo")

