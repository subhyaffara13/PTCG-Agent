
def test_nonsquare():
    A = MatrixSymbol('A', 2, 3)
    B = ImmutableMatrix([[1, 2, 3], [4, 5, 6]])
    for r in [-1, 0, 1, 2, S.Half, S.Pi, n]:
        raises(NonSquareMatrixError, lambda: MatPow(A, r))
        raises(NonSquareMatrixError, lambda: MatPow(B, r))

