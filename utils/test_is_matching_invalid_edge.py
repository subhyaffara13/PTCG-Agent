
def test_is_matching_invalid_edge(fn, edgeset):
    """All is_*matching functions have consistent exception message for invalid
    edges in matching."""
    G = nx.path_graph(4)
    with pytest.raises(nx.NetworkXError, match=".*non-2-tuple edge.*"):
        fn(G, edgeset)

