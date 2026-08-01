
def test_conjugacy_class():
    S = SymmetricGroup(4)
    x = Permutation(1, 2, 3)
    C = {Permutation(0, 1, 2, size = 4), Permutation(0, 1, 3),
             Permutation(0, 2, 1, size = 4), Permutation(0, 2, 3),
             Permutation(0, 3, 1), Permutation(0, 3, 2),
             Permutation(1, 2, 3), Permutation(1, 3, 2)}
    assert S.conjugacy_class(x) == C

