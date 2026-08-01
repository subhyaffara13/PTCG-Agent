
def test_sympy__matrices__expressions__trace__Trace():
    from sympy.matrices.expressions.trace import Trace
    from sympy.matrices.expressions import MatrixSymbol
    assert _test_args(Trace(MatrixSymbol('A', 3, 3)))

