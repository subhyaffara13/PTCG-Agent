
def test_KroneckerProduct_entry():
    A = MatrixSymbol('A', n, m)
    B = MatrixSymbol('B', o, p)

    assert KroneckerProduct(A, B)._entry(i, j) == A[Mod(floor(i/o), n), Mod(floor(j/p), m)]*B[Mod(i, o), Mod(j, p)]

