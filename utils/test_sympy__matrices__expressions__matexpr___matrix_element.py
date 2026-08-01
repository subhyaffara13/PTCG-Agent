
def test_sympy__matrices__expressions__matexpr__MatrixElement():
    from sympy.matrices.expressions.matexpr import MatrixSymbol, MatrixElement
    from sympy.core.singleton import S
    assert _test_args(MatrixElement(MatrixSymbol('A', 3, 5), S(2), S(3)))

