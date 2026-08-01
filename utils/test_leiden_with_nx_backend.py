
def test_leiden_with_nx_backend():
    G = nx.karate_club_graph()
    with pytest.raises(NotImplementedError):
        nx.community.leiden_partitions(G, backend="networkx")
    with pytest.raises(NotImplementedError):
        nx.community.leiden_communities(G, backend="networkx")

