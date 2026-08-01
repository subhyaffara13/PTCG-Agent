
def test_multi_sequence():
    # Test nongraphical multi sequence
    seq = [1000, 3, 3, 3, 3, 2, 2, 2, 1, 1]
    assert not nx.is_multigraphical(seq)
    # Test small graphical multi sequence
    seq = [6, 5, 4, 4, 2, 1, 1, 1]
    assert nx.is_multigraphical(seq)
    # Test for negative integer in sequence
    seq = [6, 5, 4, -4, 2, 1, 1, 1]
    assert not nx.is_multigraphical(seq)
    # Test for sequence with odd sum
    seq = [1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 4]
    assert not nx.is_multigraphical(seq)
    # Test for noninteger
    seq = [1, 1, 1.1, 1]
    assert not nx.is_multigraphical(seq)
    seq = [1, 1, "rer", 1]
    assert not nx.is_multigraphical(seq)

