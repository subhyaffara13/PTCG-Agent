
def test_KroneckerProduct_combine_mul():
    X = MatrixSymbol('X', m, n)
    Y = MatrixSymbol('Y', m, n)
    kp1 = kronecker_product(A, X)
    kp2 = kronecker_product(B, Y)
    assert combine_kronecker(kp1+kp2) == kronecker_product(A+B, X+Y)

