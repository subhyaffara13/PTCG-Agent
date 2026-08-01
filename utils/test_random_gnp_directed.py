
def test_random_gnp_directed():
    # seeds = [3894723670, 500186844, 267231174, 2181982262, 1116750056]
    seeds = [21]
    for seed in seeds:
        G = nx.gnp_random_graph(20, 0.2, directed=True, seed=seed)
        _check_edge_connectivity(G)

