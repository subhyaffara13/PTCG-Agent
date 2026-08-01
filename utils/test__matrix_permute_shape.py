
def test_MatrixPermute_shape():
    p = Permutation(0, 1)
    A = MatrixSymbol('A', 2, 3)
    assert MatrixPermute(A, p).shape == (2, 3)

