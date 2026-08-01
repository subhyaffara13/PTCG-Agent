
def test_polycyclic():
    a = Permutation([0, 1, 2])
    b = Permutation([2, 1, 0])
    G = PermutationGroup([a, b])
    assert G.is_polycyclic is True

    a = Permutation([1, 2, 3, 4, 0])
    b = Permutation([1, 0, 2, 3, 4])
    G = PermutationGroup([a, b])
    assert G.is_polycyclic is False

