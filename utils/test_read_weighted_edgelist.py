
def test_read_weighted_edgelist():
    bytesIO = io.BytesIO(edges_with_values.encode("utf-8"))
    G = nx.read_weighted_edgelist(bytesIO, nodetype=int)
    assert edges_equal(G.edges(data=True), _expected_edges_weights)

