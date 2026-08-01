
def test_binomial_tree_broadcast(n):
    G = nx.binomial_tree(n)
    b_T, b_C = nx.tree_broadcast_center(G)
    assert b_T == n
    assert b_C == {0, 2 ** (n - 1)}
    assert nx.tree_broadcast_time(G) == 2 * n - 1

