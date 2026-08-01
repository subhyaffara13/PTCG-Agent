
def test_one_exchange_optimal():
    # Greedy one exchange should find the optimal solution for this graph (14)
    G = nx.Graph()
    G.add_edge(1, 2, weight=3)
    G.add_edge(1, 3, weight=3)
    G.add_edge(1, 4, weight=3)
    G.add_edge(1, 5, weight=3)
    G.add_edge(2, 3, weight=5)

    cut_size, (set1, set2) = maxcut.one_exchange(G, weight="weight", seed=5)

    _is_valid_cut(G, set1, set2)
    _cut_is_locally_optimal(G, cut_size, set1)
    # check global optimality
    assert cut_size == 14

