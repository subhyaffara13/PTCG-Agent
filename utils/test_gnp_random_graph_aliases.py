
def test_gnp_random_graph_aliases(generator, seed, directed, expected_num_edges):
    """Test that aliases give the same result with the same seed."""
    G = generator(100, 0.25, seed=seed, directed=directed)
    assert len(G) == 100
    assert G.number_of_edges() == expected_num_edges
    assert G.is_directed() == directed

