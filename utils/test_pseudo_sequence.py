
def test_pseudo_sequence():
    # Test small valid pseudo sequence
    seq = [1000, 3, 3, 3, 3, 2, 2, 2, 1, 1]
    assert nx.is_pseudographical(seq)
    # Test for sequence with odd sum
    seq = [1000, 3, 3, 3, 3, 2, 2, 2, 1, 1, 1]
    assert not nx.is_pseudographical(seq)
    # Test for negative integer in sequence
    seq = [1000, 3, 3, 3, 3, 2, 2, -2, 1, 1]
    assert not nx.is_pseudographical(seq)
    # Test for noninteger
    seq = [1, 1, 1.1, 1]
    assert not nx.is_pseudographical(seq)
    seq = [1, 1, "rer", 1]
    assert not nx.is_pseudographical(seq)

