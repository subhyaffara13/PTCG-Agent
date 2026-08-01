
def test_sympy__codegen__cfunctions__Sqrt():
    from sympy.codegen.cfunctions import Sqrt
    assert _test_args(Sqrt(x))

