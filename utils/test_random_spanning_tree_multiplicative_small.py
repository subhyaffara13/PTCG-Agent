
def test_random_spanning_tree_multiplicative_small():
    """
    Using a fixed seed, sample one tree for repeatability.
    """
    from math import exp

    pytest.importorskip("scipy")

    gamma = {
        (0, 1): -0.6383,
        (0, 2): -0.6827,
        (0, 5): 0,
        (1, 2): -1.0781,
        (1, 4): 0,
        (2, 3): 0,
        (5, 3): -0.2820,
        (5, 4): -0.3327,
        (4, 3): -0.9927,
    }

    # The undirected support of gamma
    G = nx.Graph()
    for u, v in gamma:
        G.add_edge(u, v, lambda_key=exp(gamma[(u, v)]))

    solution_edges = [(2, 3), (3, 4), (0, 5), (5, 4), (4, 1)]
    solution = nx.Graph()
    solution.add_edges_from(solution_edges)

    sampled_tree = nx.random_spanning_tree(G, "lambda_key", seed=42)

    assert nx.utils.edges_equal(solution.edges, sampled_tree.edges)

