
def test_paley_graph(p):
    """Test for the :func:`networkx.paley_graph` function."""
    G = nx.paley_graph(p)
    # G has p nodes
    assert len(G) == p
    # G is (p-1)/2-regular
    in_degrees = {G.in_degree(node) for node in G.nodes}
    out_degrees = {G.out_degree(node) for node in G.nodes}
    assert len(in_degrees) == 1 and in_degrees.pop() == (p - 1) // 2
    assert len(out_degrees) == 1 and out_degrees.pop() == (p - 1) // 2

    # If p = 1 mod 4, -1 is a square mod 4 and therefore the
    # edge in the Paley graph are symmetric.
    if p % 4 == 1:
        for u, v in G.edges:
            assert (v, u) in G.edges

