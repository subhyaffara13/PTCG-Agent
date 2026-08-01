
def test_cartesian_product_raises():
    with pytest.raises(nx.NetworkXError):
        P = nx.cartesian_product(nx.DiGraph(), nx.Graph())

