
def test_value_error(k):
    """
    Check that invalid values of k raise (must be between 1 and n - 1, inclusive,
    and such that the probability is between 0 and 1, exclusive).
    """
    G = nx.path_graph(5)
    with pytest.raises(ValueError, match=r"invalid number of communities"):
        nx.non_randomness(G, k=k)

