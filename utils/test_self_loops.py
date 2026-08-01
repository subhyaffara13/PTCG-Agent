
def test_self_loops():
    G = nx.Graph()
    G.add_edge(1, 2)
    G.add_edge(1, 1)
    with pytest.raises(nx.NetworkXError, match="Graph must not contain self-loops"):
        nx.non_randomness(G)


def test_self_loops():
    """A tournament must have no self-loops."""
    G = DiGraph()
    G.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 0), (1, 3), (0, 2)])
    G.add_edge(0, 0)
    assert not is_tournament(G)

