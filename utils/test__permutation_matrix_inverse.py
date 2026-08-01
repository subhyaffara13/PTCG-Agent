
def test_PermutationMatrix_inverse():
    P = PermutationMatrix(Permutation(0, 1, 2))
    assert Inverse(P).doit() == PermutationMatrix(Permutation(0, 2, 1))

