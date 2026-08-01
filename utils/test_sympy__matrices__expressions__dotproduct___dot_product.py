
def test_sympy__matrices__expressions__dotproduct__DotProduct():
    from sympy.matrices.expressions.dotproduct import DotProduct
    from sympy.matrices.expressions import MatrixSymbol
    X = MatrixSymbol('X', x, 1)
    Y = MatrixSymbol('Y', x, 1)
    assert _test_args(DotProduct(X, Y))

