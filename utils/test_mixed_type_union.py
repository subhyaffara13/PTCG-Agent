
def test_mixed_type_union():
    with pytest.raises(nx.NetworkXError):
        G = nx.Graph()
        H = nx.MultiGraph()
        I = nx.Graph()
        U = nx.union_all([G, H, I])
    with pytest.raises(nx.NetworkXError):
        X = nx.Graph()
        Y = nx.DiGraph()
        XY = nx.union_all([X, Y])


def test_mixed_type_union():
    G = nx.Graph()
    H = nx.MultiGraph()
    pytest.raises(nx.NetworkXError, nx.union, G, H)
    pytest.raises(nx.NetworkXError, nx.disjoint_union, G, H)
    pytest.raises(nx.NetworkXError, nx.intersection, G, H)
    pytest.raises(nx.NetworkXError, nx.difference, G, H)
    pytest.raises(nx.NetworkXError, nx.symmetric_difference, G, H)
    pytest.raises(nx.NetworkXError, nx.compose, G, H)

