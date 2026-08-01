
def test_PermutationMatrix_matpow():
    p1 = Permutation([1, 2, 0])
    P1 = PermutationMatrix(p1)
    p2 = Permutation([2, 0, 1])
    P2 = PermutationMatrix(p2)
    assert P1**2 == P2
    assert P1**3 == Identity(3)

