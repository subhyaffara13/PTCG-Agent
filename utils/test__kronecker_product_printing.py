
def test_KroneckerProduct_printing():
    A = MatrixSymbol('A', 3, 3)
    B = MatrixSymbol('B', 2, 2)
    assert latex(KroneckerProduct(A, B)) == r'A \otimes B'

