
def test_resolution():
    G = nx.LFR_benchmark_graph(
        250, 3, 1.5, 0.009, average_degree=5, min_community=20, seed=10
    )

    partition1 = nx.community.leiden_communities(G, resolution=0.5, seed=12)
    partition2 = nx.community.leiden_communities(G, seed=12)
    partition3 = nx.community.leiden_communities(G, resolution=2, seed=12)

    assert len(partition1) <= len(partition2)
    assert len(partition2) <= len(partition3)


def test_resolution():
    G = nx.LFR_benchmark_graph(
        250, 3, 1.5, 0.009, average_degree=5, min_community=20, seed=10
    )

    partition1 = nx.community.louvain_communities(G, resolution=0.5, seed=12)
    partition2 = nx.community.louvain_communities(G, seed=12)
    partition3 = nx.community.louvain_communities(G, resolution=2, seed=12)

    assert len(partition1) <= len(partition2) <= len(partition3)

