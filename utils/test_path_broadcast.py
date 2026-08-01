
def test_path_broadcast(n):
    G = nx.path_graph(n)
    b_T, b_C = nx.tree_broadcast_center(G)
    assert b_T == math.ceil(n / 2)
    assert b_C == {
        math.ceil(n / 2),
        n // 2,
        math.ceil(n / 2 - 1),
        n // 2 - 1,
    }
    assert nx.tree_broadcast_time(G) == n - 1

