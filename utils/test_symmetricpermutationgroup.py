
def test_symmetricpermutationgroup():
    a = SymmetricPermutationGroup(5)
    assert a.degree == 5
    assert a.order() == 120
    assert a.identity() == Permutation(4)

