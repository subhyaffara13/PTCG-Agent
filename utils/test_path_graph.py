
def test_path_graph():
    G = nx.path_graph(4)
    answer = {0: 0.5, 1: 0.5, 2: 0.5, 3: 0.5}
    assert bipartite.clustering(G, mode="dot") == answer
    assert bipartite.clustering(G, mode="max") == answer
    answer = {0: 1, 1: 1, 2: 1, 3: 1}
    assert bipartite.clustering(G, mode="min") == answer

