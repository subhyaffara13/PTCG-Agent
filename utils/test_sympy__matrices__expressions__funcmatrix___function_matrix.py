
def test_sympy__matrices__expressions__funcmatrix__FunctionMatrix():
    from sympy.matrices.expressions.funcmatrix import FunctionMatrix
    from sympy.core.symbol import symbols
    i, j = symbols('i,j')
    assert _test_args(FunctionMatrix(3, 3, Lambda((i, j), i - j) ))

