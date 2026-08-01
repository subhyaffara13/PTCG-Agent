
def test_sympy__codegen__cfunctions__expm1():
    from sympy.codegen.cfunctions import expm1
    assert _test_args(expm1(x))

