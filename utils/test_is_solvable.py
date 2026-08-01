
def test_is_solvable():
    a = Permutation([1, 2, 0])
    b = Permutation([1, 0, 2])
    G = PermutationGroup([a, b])
    assert G.is_solvable
    G = PermutationGroup([a])
    assert G.is_solvable
    a = Permutation([1, 2, 3, 4, 0])
    b = Permutation([1, 0, 2, 3, 4])
    G = PermutationGroup([a, b])
    assert not G.is_solvable
    P = SymmetricGroup(10)
    S = P.sylow_subgroup(3)
    assert S.is_solvable

