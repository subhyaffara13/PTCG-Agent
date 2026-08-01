
def test_configuration_directed():
    # seeds = [671221681, 2403749451, 124433910, 672335939, 1193127215]
    seeds = [67]
    for seed in seeds:
        deg_seq = nx.random_powerlaw_tree_sequence(20, seed=seed, tries=5000)
        G = nx.DiGraph(nx.configuration_model(deg_seq, seed=seed))
        G.remove_edges_from(nx.selfloop_edges(G))
        _check_edge_connectivity(G)

