
def test_scale_free_graph_negative_delta():
    with pytest.raises(ValueError, match="delta_in must be >= 0."):
        scale_free_graph(10, delta_in=-1)
    with pytest.raises(ValueError, match="delta_out must be >= 0."):
        scale_free_graph(10, delta_out=-1)

