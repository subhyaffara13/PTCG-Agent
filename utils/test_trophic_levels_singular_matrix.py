
def test_trophic_levels_singular_matrix():
    """Should raise an error with graphs with only non-basal nodes"""
    matrix = np.identity(4)
    G = nx.from_numpy_array(matrix, create_using=nx.DiGraph)
    with pytest.raises(nx.NetworkXError, match="no basal nodes"):
        nx.trophic_levels(G)

