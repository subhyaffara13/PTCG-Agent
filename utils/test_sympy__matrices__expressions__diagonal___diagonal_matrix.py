
def test_sympy__matrices__expressions__diagonal__DiagonalMatrix():
    from sympy.matrices.expressions.diagonal import DiagonalMatrix
    from sympy.matrices.expressions import MatrixSymbol
    x = MatrixSymbol('x', 10, 1)
    assert _test_args(DiagonalMatrix(x))

