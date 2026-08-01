
def test_asadpour_empty_graph():
    """
    Test the asadpour_atsp function with an empty graph
    """
    G = nx.DiGraph()

    pytest.raises(nx.NetworkXError, nx_app.asadpour_atsp, G)

