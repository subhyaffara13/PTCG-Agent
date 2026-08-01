
def test_isomorphism_iter2():
    # Path
    for L in range(2, 10):
        g1 = nx.path_graph(L)
        gm = iso.GraphMatcher(g1, g1)
        s = len(list(gm.isomorphisms_iter()))
        assert s == 2
    # Cycle
    for L in range(3, 10):
        g1 = nx.cycle_graph(L)
        gm = iso.GraphMatcher(g1, g1)
        s = len(list(gm.isomorphisms_iter()))
        assert s == 2 * L

