
def test_is_primitive():
    S = SymmetricGroup(5)
    assert S.is_primitive() is True
    C = CyclicGroup(7)
    assert C.is_primitive() is True

    a = Permutation(0, 1, 2, size=6)
    b = Permutation(3, 4, 5, size=6)
    G = PermutationGroup(a, b)
    assert G.is_primitive() is False

