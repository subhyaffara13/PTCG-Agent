
def test_random_gnp():
    # seeds = [1550709854, 1309423156, 4208992358, 2785630813, 1915069929]
    seeds = [12, 13]

    for seed in seeds:
        G = nx.gnp_random_graph(20, 0.2, seed=seed)
        _check_edge_connectivity(G)


def test_random_gnp(n, p):
    G = nx.gnp_random_graph(n, p, seed=42)
    result = nx.k_components(G)
    _check_connectivity(G, result)


def test_random_gnp():
    G = nx.gnp_random_graph(100, 0.1, seed=42)
    _check_separating_sets(G)

