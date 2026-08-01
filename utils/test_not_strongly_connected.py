
def test_not_strongly_connected():
    """Tests for a tournament that is not strongly connected."""
    G = DiGraph([(0, 1), (0, 2), (1, 2)])
    assert not is_strongly_connected(G)

