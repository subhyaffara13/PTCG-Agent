
def test_expected_degree_graph_selfloops():
    deg_seq = [3] * 12
    G1 = nx.expected_degree_graph(deg_seq, seed=1000, selfloops=False)
    G2 = nx.expected_degree_graph(deg_seq, seed=1000, selfloops=False)
    assert len(G1) == len(G2) == len(deg_seq)
    assert nx.is_isomorphic(G1, G2)
    assert nx.number_of_selfloops(G1) == nx.number_of_selfloops(G2) == 0

