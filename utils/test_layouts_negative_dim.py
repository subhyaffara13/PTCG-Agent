
def test_layouts_negative_dim(layout):
    """Test all layouts that support dim kwarg handle invalid inputs."""
    G = nx.path_graph(4)
    valid_err_msgs = "|".join(
        [
            "negative dimensions.*not allowed",
            "can only handle 2",
            "cannot handle.*2",
        ]
    )
    with pytest.raises(ValueError, match=valid_err_msgs):
        layout(G, dim=-1)

