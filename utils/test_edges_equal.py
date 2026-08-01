
def test_edges_equal(n, gen, create_using):
    """Test whether edges_equal properly compares edges without attribute data."""
    G = gen(n, create_using=create_using)
    H = gen(n, create_using=create_using)
    assert edges_equal(G.edges(), H.edges(), directed=G.is_directed())
    assert edges_equal(H.edges(), G.edges(), directed=H.is_directed())

    H.remove_edge(0, 1)
    assert edges_equal(H.edges(), H.edges(), directed=H.is_directed())
    assert not edges_equal(G.edges(), H.edges(), directed=G.is_directed())
    assert not edges_equal(H.edges(), G.edges(), directed=H.is_directed())

