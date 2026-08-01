
def test_rooted_product_raises():
    with pytest.raises(nx.NodeNotFound):
        nx.rooted_product(nx.Graph(), nx.path_graph(2), 10)

