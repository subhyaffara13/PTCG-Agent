
def test_bridge():
    G = nx.Graph([(2393, 2257), (2393, 2685), (2685, 2257), (1758, 2257)])
    _check_augmentations(G)

