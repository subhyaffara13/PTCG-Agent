
def test_random_partitioning():
    G = nx.complete_graph(5)
    _, (set1, set2) = maxcut.randomized_partitioning(G, seed=5)
    _is_valid_cut(G, set1, set2)

