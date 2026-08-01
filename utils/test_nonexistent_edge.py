
def test_nonexistent_edge():
    """Tests that attempting to contract a nonexistent edge raises an
    exception.

    """
    G = nx.cycle_graph(4)
    with pytest.raises(ValueError):
        nx.contracted_edge(G, (0, 2))

