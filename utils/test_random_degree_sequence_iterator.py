
def test_random_degree_sequence_iterator():
    G1 = nx.fast_gnp_random_graph(100, 0.1, seed=42)
    d1 = (d for n, d in G1.degree())
    G2 = nx.random_degree_sequence_graph(d1, seed=42)
    assert len(G2) > 0

