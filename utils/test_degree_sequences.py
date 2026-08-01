
def test_degree_sequences():
    seq = nx.utils.powerlaw_sequence(10, seed=1)
    seq = nx.utils.powerlaw_sequence(10)
    assert len(seq) == 10

