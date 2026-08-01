
def test_expected_degree_graph_empty():
    # empty graph has empty degree sequence
    deg_seq = []
    G = nx.expected_degree_graph(deg_seq)
    assert dict(G.degree()) == {}

