
def test_reverse1():
    # Other tests for reverse are done by the DiGraph and MultiDigraph.
    G1 = nx.Graph()
    pytest.raises(nx.NetworkXError, nx.reverse, G1)

