
def test_bad_k():
    with pytest.raises(nx.NetworkXError):
        list(nx.community.k_clique_communities(nx.Graph(), 1))

