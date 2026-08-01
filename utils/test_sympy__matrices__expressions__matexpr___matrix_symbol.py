
def test_sympy__matrices__expressions__matexpr__MatrixSymbol():
    from sympy.matrices.expressions.matexpr import MatrixSymbol
    assert _test_args(MatrixSymbol('A', 3, 5))

