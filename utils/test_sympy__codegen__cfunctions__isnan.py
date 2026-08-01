
def test_sympy__codegen__cfunctions__isnan():
    from sympy.codegen.cfunctions import isnan
    assert _test_args(isnan(x))

