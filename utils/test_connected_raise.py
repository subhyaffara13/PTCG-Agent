
def test_connected_raise():
    DG = nx.DiGraph()
    with pytest.raises(NetworkXNotImplemented):
        next(nx.biconnected_components(DG))
    with pytest.raises(NetworkXNotImplemented):
        next(nx.biconnected_component_edges(DG))
    with pytest.raises(NetworkXNotImplemented):
        next(nx.articulation_points(DG))
    pytest.raises(NetworkXNotImplemented, nx.is_biconnected, DG)

