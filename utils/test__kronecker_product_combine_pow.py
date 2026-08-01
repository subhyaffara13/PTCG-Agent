
def test_KroneckerProduct_combine_pow():
    X = MatrixSymbol('X', n, n)
    Y = MatrixSymbol('Y', n, n)
    assert combine_kronecker(KroneckerProduct(
        X, Y)**x) == KroneckerProduct(X**x, Y**x)
    assert combine_kronecker(x * KroneckerProduct(X, Y)
                             ** 2) == x * KroneckerProduct(X**2, Y**2)
    assert combine_kronecker(
        x * (KroneckerProduct(X, Y)**2) * KroneckerProduct(A, B)) == x * KroneckerProduct(X**2 * A, Y**2 * B)
    # cannot simplify because of non-square arguments to kronecker product:
    assert combine_kronecker(KroneckerProduct(A, B.T) ** m) == KroneckerProduct(A, B.T) ** m

