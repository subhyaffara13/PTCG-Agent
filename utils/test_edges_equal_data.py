
def test_edges_equal_data():
    """Test whether ``edges_equal`` properly compares edges with attribute dictionaries."""
    G = nx.path_graph(3)
    H = nx.path_graph(3)
    I = nx.path_graph(3, create_using=nx.MultiGraph)

    attrs = {(0, 1): {"attr1": 20, "attr2": "nothing"}, (1, 2): {"attr2": 3}}
    nx.set_edge_attributes(G, attrs)
    assert edges_equal(G.edges(data=True), G.edges(data=True))
    assert not edges_equal(G.edges(data=True), G.edges())

    nx.set_edge_attributes(H, attrs)
    assert edges_equal(G.edges(), H.edges())
    assert edges_equal(G.edges(data=True), H.edges(data=True))

    H[0][1]["attr2"] = "something"
    assert edges_equal(G.edges(), H.edges())
    assert not edges_equal(G.edges(data=True), H.edges(data=True))

