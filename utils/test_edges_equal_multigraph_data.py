
def test_edges_equal_multigraph_data():
    """Test whether ``edges_equal`` properly compares edges with attribute dictionaries in ``MultiGraphs``."""
    G = nx.path_graph(3, create_using=nx.MultiGraph)
    I = nx.path_graph(3, create_using=nx.MultiGraph)

    G.add_edge(0, 1, 0, attr1="blue")
    G.add_edge(1, 2, 1, attr2="green")
    I.add_edge(0, 1, 0, attr1="blue")
    I.add_edge(0, 1, 1, attr2="green")
    assert edges_equal(G.edges(data=True), G.edges(data=True))
    assert not edges_equal(G.edges(), I.edges())
    assert not edges_equal(G.edges(data=True), I.edges(data=True))
    assert not edges_equal(G.edges(keys=True), I.edges(keys=True))
    assert not edges_equal(G.edges(keys=True, data=True), I.edges(keys=True, data=True))

