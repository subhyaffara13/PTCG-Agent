
def test_valid_degree_sequence(deg_seq, valid, reason):
    v, r = nx.utils.is_valid_tree_degree_sequence(deg_seq)
    assert v == valid
    assert reason in r

