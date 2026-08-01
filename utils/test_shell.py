
def test_shell():
    # seeds = [2057382236, 3331169846, 1840105863, 476020778, 2247498425]
    seeds = [18]
    for seed in seeds:
        constructor = [(12, 70, 0.8), (15, 40, 0.6)]
        G = nx.random_shell_graph(constructor, seed=seed)
        _check_augmentations(G)


def test_shell():
    # seeds = [2057382236, 3331169846, 1840105863, 476020778, 2247498425]
    seeds = [20]
    for seed in seeds:
        constructor = [(12, 70, 0.8), (15, 40, 0.6)]
        G = nx.random_shell_graph(constructor, seed=seed)
        _check_edge_connectivity(G)


def test_shell(constructor):
    G = nx.random_shell_graph(constructor, seed=42)
    result = nx.k_components(G)
    _check_connectivity(G, result)


def test_shell():
    constructor = [(20, 80, 0.8), (80, 180, 0.6)]
    G = nx.random_shell_graph(constructor, seed=42)
    _check_separating_sets(G)

