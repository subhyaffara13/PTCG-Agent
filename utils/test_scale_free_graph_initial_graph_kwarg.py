
def test_scale_free_graph_initial_graph_kwarg(ig):
    with pytest.raises(nx.NetworkXError):
        scale_free_graph(100, initial_graph=ig)

