
def test_PermutationMatrix_basic():
    p = Permutation([1, 0])
    assert unchanged(PermutationMatrix, p)
    raises(ValueError, lambda: PermutationMatrix((0, 1, 2)))
    assert PermutationMatrix(p).as_explicit() == Matrix([[0, 1], [1, 0]])
    assert isinstance(PermutationMatrix(p)*MatrixSymbol('A', 2, 2), MatMul)

