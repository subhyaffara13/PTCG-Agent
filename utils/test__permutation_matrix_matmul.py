
def test_PermutationMatrix_matmul():
    p = Permutation([1, 2, 0])
    P = PermutationMatrix(p)
    M = Matrix([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
    assert (P*M).as_explicit() == P.as_explicit()*M
    assert (M*P).as_explicit() == M*P.as_explicit()

    P1 = PermutationMatrix(Permutation([1, 2, 0]))
    P2 = PermutationMatrix(Permutation([2, 1, 0]))
    P3 = PermutationMatrix(Permutation([1, 0, 2]))
    assert P1*P2 == P3

