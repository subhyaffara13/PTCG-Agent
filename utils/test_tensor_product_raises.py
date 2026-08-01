
def test_tensor_product_raises():
    with pytest.raises(nx.NetworkXError):
        P = nx.tensor_product(nx.DiGraph(), nx.Graph())

