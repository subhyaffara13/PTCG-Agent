
def test_configuration():
    # seeds = [2718183590, 2470619828, 1694705158, 3001036531, 2401251497]
    seeds = [1001, 1002, 1003, 1004]
    for seed in seeds:
        deg_seq = nx.random_powerlaw_tree_sequence(20, seed=seed, tries=5000)
        G = nx.Graph(nx.configuration_model(deg_seq, seed=seed))
        G.remove_edges_from(nx.selfloop_edges(G))
        _check_augmentations(G)


def test_configuration():
    # seeds = [2718183590, 2470619828, 1694705158, 3001036531, 2401251497]
    seeds = [14, 15]
    for seed in seeds:
        deg_seq = nx.random_powerlaw_tree_sequence(20, seed=seed, tries=5000)
        G = nx.Graph(nx.configuration_model(deg_seq, seed=seed))
        G.remove_edges_from(nx.selfloop_edges(G))
        _check_edge_connectivity(G)


def test_configuration():
    deg_seq = nx.random_powerlaw_tree_sequence(100, tries=5, seed=72)
    G = nx.Graph(nx.configuration_model(deg_seq))
    G.remove_edges_from(nx.selfloop_edges(G))
    result = nx.k_components(G)
    _check_connectivity(G, result)


def test_configuration():
    deg_seq = nx.random_powerlaw_tree_sequence(100, tries=5, seed=72)
    G = nx.Graph(nx.configuration_model(deg_seq))
    G.remove_edges_from(nx.selfloop_edges(G))
    _check_separating_sets(G)

