
def test_connected_watts_strogatz_graph_disconnected():
    """Test that `connected_watts_strogatz_graph` properly loops when disconnected."""
    with pytest.raises(nx.NetworkXError, match="Maximum number of tries exceeded"):
        nx.connected_watts_strogatz_graph(10, 0, 0.0)

