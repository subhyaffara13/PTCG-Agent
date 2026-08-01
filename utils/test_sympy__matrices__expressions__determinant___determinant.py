
def test_sympy__matrices__expressions__determinant__Determinant():
    from sympy.matrices.expressions.determinant import Determinant
    from sympy.matrices.expressions import MatrixSymbol
    assert _test_args(Determinant(MatrixSymbol('A', 3, 3)))

