
def test_is_matching_node_not_in_G(fn, edgeset):
    """All is_*matching functions have consistent exception message for node
    not in G."""
    G = nx.path_graph(4)
    with pytest.raises(nx.NetworkXError, match="matching.*with node not in G"):
        fn(G, edgeset)

