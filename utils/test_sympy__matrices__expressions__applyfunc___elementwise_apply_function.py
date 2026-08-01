
def test_sympy__matrices__expressions__applyfunc__ElementwiseApplyFunction():
    from sympy.matrices.expressions.applyfunc import ElementwiseApplyFunction
    from sympy.matrices.expressions import MatrixSymbol
    X = MatrixSymbol("X", x, x)
    func = Lambda(x, x**2)
    assert _test_args(ElementwiseApplyFunction(func, X))

