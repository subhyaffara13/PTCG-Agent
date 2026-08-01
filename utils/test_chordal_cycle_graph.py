
def test_chordal_cycle_graph(p):
    """Test for the :func:`networkx.chordal_cycle_graph` function."""
    G = nx.chordal_cycle_graph(p)
    assert len(G) == p

