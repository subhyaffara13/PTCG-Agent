
def test_sympy__codegen__cfunctions__isinf():
    from sympy.codegen.cfunctions import isinf
    assert _test_args(isinf(x))

