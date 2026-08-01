
def test_sympy__matrices__expressions__hadamard__HadamardPower():
    from sympy.matrices.expressions.hadamard import HadamardPower
    from sympy.matrices.expressions import MatrixSymbol
    from sympy.core.symbol import Symbol
    X = MatrixSymbol('X', x, y)
    n = Symbol("n")
    assert _test_args(HadamardPower(X, n))

