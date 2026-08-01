
def test_elementary():
    a = Permutation([1, 5, 2, 0, 3, 6, 4])
    G = PermutationGroup([a])
    assert G.is_elementary(7) is False

    a = Permutation(0, 1)(2, 3)
    b = Permutation(0, 2)(3, 1)
    G = PermutationGroup([a, b])
    assert G.is_elementary(2) is True
    c = Permutation(4, 5, 6)
    G = PermutationGroup([a, b, c])
    assert G.is_elementary(2) is False

    G = SymmetricGroup(4).sylow_subgroup(2)
    assert G.is_elementary(2) is False
    H = AlternatingGroup(4).sylow_subgroup(2)
    assert H.is_elementary(2) is True

