
def test_star_broadcast(n):
    G = nx.star_graph(n)
    b_T, b_C = nx.tree_broadcast_center(G)
    assert b_T == n
    assert b_C == set(G.nodes())
    assert nx.tree_broadcast_time(G) == b_T

