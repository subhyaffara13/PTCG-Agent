
def test_shortest_simple_paths_with_none_weight_function():
    def cost(u, v, x):
        delta = abs(u - v)
        # ignore interior edges
        return 1 if (delta == 1 or delta == 4) else None

    G = nx.complete_graph(5)
    paths = nx.shortest_simple_paths(G, 0, 2, weight=cost)
    assert list(paths) == [[0, 1, 2], [0, 4, 3, 2]]

