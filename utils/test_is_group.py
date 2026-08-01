
def test_is_group():
    assert PermutationGroup(Permutation(1,2), Permutation(2,4)).is_group is True
    assert SymmetricGroup(4).is_group is True

