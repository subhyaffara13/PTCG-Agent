
def test_expected_degree_graph(seed, deg_seq):
    G1 = nx.expected_degree_graph(deg_seq, seed=seed)
    G2 = nx.expected_degree_graph(deg_seq, seed=seed)
    assert len(G1) == len(G2) == len(deg_seq)
    assert nx.is_isomorphic(G1, G2)

