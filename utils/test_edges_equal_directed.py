
def test_edges_equal_directed():
    """Test whether ``edges_equal`` properly compares directed edges."""
    G = nx.DiGraph([(0, 1)])
    I = nx.DiGraph([(1, 0)])

    assert edges_equal(G.edges(), I.edges(), directed=False)
    assert not edges_equal(G.edges(), I.edges(), directed=True)

