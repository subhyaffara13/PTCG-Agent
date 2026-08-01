
def test_nonsquare_error():
    A = MatrixSymbol('A', 3, 4)
    raises(NonSquareMatrixError, lambda: Inverse(A))

