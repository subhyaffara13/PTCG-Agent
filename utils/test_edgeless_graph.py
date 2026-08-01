
def test_edgeless_graph():
    G = nx.Graph()
    G.add_nodes_from([1, 2, 3, 4])
    _check_augmentations(G)

