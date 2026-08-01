
def test_edges_equal_multiedge(n, gen, create_using):
    """Test whether ``edges_equal`` properly compares edges in multigraphs."""
    G = gen(n, create_using=create_using)
    H = gen(n, create_using=create_using)

    G_edges = list(G.edges())
    G.add_edges_from(G_edges)
    H.add_edges_from(G_edges)
    assert edges_equal(G.edges(), H.edges(), directed=G.is_directed())

    H.remove_edge(0, 1)
    assert edges_equal(H.edges(), H.edges(), directed=H.is_directed())
    assert not edges_equal(G.edges(), H.edges(), directed=G.is_directed())

