
def test_shell_directed():
    # seeds = [3134027055, 4079264063, 1350769518, 1405643020, 530038094]
    seeds = [31]
    for seed in seeds:
        constructor = [(12, 70, 0.8), (15, 40, 0.6)]
        G = nx.random_shell_graph(constructor, seed=seed).to_directed()
        _check_edge_connectivity(G)

