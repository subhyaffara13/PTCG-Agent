
def test_edges_equal_directed_data():
    """Test whether ``edges_equal`` properly compares directed edges with attribute dictionaries."""
    G = nx.DiGraph()
    I = nx.DiGraph()

    G.add_edge(0, 1, attr1="blue")
    I.add_edge(0, 1, attr1="blue")
    assert edges_equal(G.edges(data=True), G.edges(data=True), directed=True)
    I.add_edge(1, 2, attr2="green")
    assert not edges_equal(G.edges(data=True), I.edges(data=True), directed=True)
    G.add_edge(1, 2, attr2="green")
    assert edges_equal(G.edges(data=True), I.edges(data=True), directed=True)
    G.remove_edge(1, 2)
    G.add_edge(2, 1, attr2="green")
    assert edges_equal(G.edges(data=True), I.edges(data=True), directed=False)
    assert not edges_equal(G.edges(data=True), I.edges(data=True), directed=True)

