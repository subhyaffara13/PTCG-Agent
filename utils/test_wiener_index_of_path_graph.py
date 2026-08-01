
def test_wiener_index_of_path_graph():
    # In P_n, there are n - 1 pairs of vertices at distance one, n -
    # 2 pairs at distance two, n - 3 at distance three, ..., 1 at
    # distance n - 1, so the Wiener index should be
    #
    #     1 * (n - 1) + 2 * (n - 2) + ... + (n - 2) * 2 + (n - 1) * 1
    #
    # For example, in P_5,
    #
    #     1 * 4 + 2 * 3 + 3 * 2 + 4 * 1 = 2 (1 * 4 + 2 * 3)
    #
    # and in P_6,
    #
    #     1 * 5 + 2 * 4 + 3 * 3 + 4 * 2 + 5 * 1 = 2 (1 * 5 + 2 * 4) + 3 * 3
    #
    # assuming n is *odd*, this gives the formula
    #
    #     2 \sum_{i = 1}^{(n - 1) / 2} [i * (n - i)]
    #
    # assuming n is *even*, this gives the formula
    #
    #     2 \sum_{i = 1}^{n / 2} [i * (n - i)] - (n / 2) ** 2
    #
    n = 9
    G = nx.path_graph(n)
    expected = 2 * sum(i * (n - i) for i in range(1, (n // 2) + 1))
    actual = nx.wiener_index(G)
    assert expected == actual

