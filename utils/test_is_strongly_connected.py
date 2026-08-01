
def test_is_strongly_connected():
    """Tests for a strongly connected tournament."""
    G = DiGraph([(0, 1), (1, 2), (2, 0)])
    assert is_strongly_connected(G)

