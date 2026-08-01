
def test_sympy__matrices__expressions__kronecker__KroneckerProduct():
    from sympy.matrices.expressions.kronecker import KroneckerProduct
    from sympy.matrices.expressions import MatrixSymbol
    X = MatrixSymbol('X', x, y)
    Y = MatrixSymbol('Y', x, y)
    assert _test_args(KroneckerProduct(X, Y))

