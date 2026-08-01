
def test_PermutationMatrix_determinant():
    P = PermutationMatrix(Permutation([0, 1, 2]))
    assert Determinant(P).doit() == 1
    P = PermutationMatrix(Permutation([0, 2, 1]))
    assert Determinant(P).doit() == -1
    P = PermutationMatrix(Permutation([2, 0, 1]))
    assert Determinant(P).doit() == 1

