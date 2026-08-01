
def test_PermutationGroup():
    assert PermutationGroup() == PermutationGroup(Permutation())
    assert (PermutationGroup() == 0) is False

