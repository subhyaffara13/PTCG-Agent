
def test_graph_power_raises():
    with pytest.raises(nx.NetworkXNotImplemented):
        nx.power(nx.MultiDiGraph(), 2)

