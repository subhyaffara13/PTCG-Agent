
def test_greedy_bipartition():
    G = nx.barbell_graph(3, 0)
    split = nx.community.greedy_node_swap_bipartition(G)
    soln = ({0, 1, 2}, {3, 4, 5})
    assert set(map(frozenset, split)) == set(map(frozenset, soln))

