
def test_inverse_non_invertible():
    raises(NonInvertibleMatrixError, lambda: ZeroMatrix(n, n).I)
    raises(NonInvertibleMatrixError, lambda: OneMatrix(2, 2).I)

