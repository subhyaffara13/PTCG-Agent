
def test_point_graph():
    G = nx.Graph()
    G.add_node(1)
    _check_augmentations(G, max_k=MAX_EFFICIENT_K + 2)

