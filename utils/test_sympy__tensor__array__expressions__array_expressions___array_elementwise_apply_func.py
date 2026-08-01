
def test_sympy__tensor__array__expressions__array_expressions__ArrayElementwiseApplyFunc():
    from sympy.tensor.array.expressions.array_expressions import ArraySymbol, ArrayElementwiseApplyFunc
    A = ArraySymbol("A", (4,))
    assert _test_args(ArrayElementwiseApplyFunc(exp, A))

