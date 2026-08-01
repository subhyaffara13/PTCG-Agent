
def test_sympy__matrices__expressions__slice__MatrixSlice():
    from sympy.matrices.expressions.slice import MatrixSlice
    from sympy.matrices.expressions import MatrixSymbol
    X = MatrixSymbol('X', 4, 4)
    assert _test_args(MatrixSlice(X, (0, 2), (0, 2)))

