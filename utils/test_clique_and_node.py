
def test_clique_and_node():
    for n in range(1, 10):
        G = nx.complete_graph(n)
        G.add_node(n + 1)
        _check_augmentations(G, max_k=MAX_EFFICIENT_K + 2)

