
def test_sympy__matrices__expressions__determinant__Permanent():
    from sympy.matrices.expressions.determinant import Permanent
    from sympy.matrices.expressions import MatrixSymbol
    assert _test_args(Permanent(MatrixSymbol('A', 3, 4)))

