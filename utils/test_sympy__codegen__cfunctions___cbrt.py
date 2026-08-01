
def test_sympy__codegen__cfunctions__Cbrt():
    from sympy.codegen.cfunctions import Cbrt
    assert _test_args(Cbrt(x))

