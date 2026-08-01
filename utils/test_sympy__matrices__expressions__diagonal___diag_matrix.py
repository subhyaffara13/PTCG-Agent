
def test_sympy__matrices__expressions__diagonal__DiagMatrix():
    from sympy.matrices.expressions.diagonal import DiagMatrix
    from sympy.matrices.expressions import MatrixSymbol
    x = MatrixSymbol('x', 10, 1)
    assert _test_args(DiagMatrix(x))

