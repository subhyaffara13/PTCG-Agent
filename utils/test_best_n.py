
def test_best_n():
    G = nx.barbell_graph(5, 3)

    # Same result as without enforcing cutoff:
    best_n = 3
    expected = [frozenset(range(5)), frozenset(range(8, 13)), frozenset(range(5, 8))]
    assert greedy_modularity_communities(G, best_n=best_n) == expected

    # One additional merging step:
    best_n = 2
    expected = [frozenset(range(8)), frozenset(range(8, 13))]
    assert greedy_modularity_communities(G, best_n=best_n) == expected

    # Two additional merging steps:
    best_n = 1
    expected = [frozenset(range(13))]
    assert greedy_modularity_communities(G, best_n=best_n) == expected

