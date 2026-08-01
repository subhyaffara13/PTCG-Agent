
def test_exception():
    assert_raises(MemoryError, _sparsetools.test_throw_error)


def test_exception():
    with pytest.raises(nx.NetworkXError):
        G = nx.MultiDiGraph()
        cytoscape_data(G, name="foo", ident="foo")

