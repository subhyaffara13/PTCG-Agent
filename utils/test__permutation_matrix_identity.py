
def test_PermutationMatrix_identity():
    p = Permutation([0, 1])
    assert PermutationMatrix(p).is_Identity

    p = Permutation([1, 0])
    assert not PermutationMatrix(p).is_Identity

