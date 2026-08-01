
def test__extrema_bounding_invalid_compute_kwarg():
    G = nx.path_graph(3)
    with pytest.raises(ValueError, match="compute must be one of"):
        _extrema_bounding(G, compute="spam")

