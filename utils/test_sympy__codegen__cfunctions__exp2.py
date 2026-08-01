
def test_sympy__codegen__cfunctions__exp2():
    from sympy.codegen.cfunctions import exp2
    assert _test_args(exp2(x))

