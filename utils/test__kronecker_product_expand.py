
def test_KroneckerProduct_expand():
    X = MatrixSymbol('X', n, n)
    Y = MatrixSymbol('Y', n, n)

    assert KroneckerProduct(X + Y, Y + Z).expand(kroneckerproduct=True) == \
        KroneckerProduct(X, Y) + KroneckerProduct(X, Z) + \
        KroneckerProduct(Y, Y) + KroneckerProduct(Y, Z)

