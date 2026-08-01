
def test_cliques():
    for n in range(1, 10):
        G = nx.complete_graph(n)
        _check_augmentations(G, max_k=MAX_EFFICIENT_K + 2)

