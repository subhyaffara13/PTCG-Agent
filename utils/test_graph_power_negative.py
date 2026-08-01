
def test_graph_power_negative():
    with pytest.raises(ValueError):
        nx.power(nx.Graph(), -1)

