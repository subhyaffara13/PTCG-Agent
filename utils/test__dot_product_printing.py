
def test_DotProduct_printing():
    X = MatrixSymbol('X', 3, 1)
    Y = MatrixSymbol('Y', 3, 1)
    a = Symbol('a')
    assert latex(DotProduct(X, Y)) == r"X \cdot Y"
    assert latex(DotProduct(a * X, Y)) == r"a X \cdot Y"
    assert latex(a * DotProduct(X, Y)) == r"a \left(X \cdot Y\right)"

