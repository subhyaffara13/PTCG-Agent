
def test_gnp_generators_negative_edge_probability(generator, directed):
    """If the edge probability `p` is <=0, the resulting graph should have no edges."""
    G = generator(10, -1.1, directed=directed)
    assert len(G) == 10
    assert G.number_of_edges() == 0
    assert G.is_directed() == directed

