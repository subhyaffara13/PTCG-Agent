
def test_sympy__codegen__pynodes__NumExprEvaluate():
    from sympy.codegen.pynodes import NumExprEvaluate
    assert _test_args(NumExprEvaluate(x))

