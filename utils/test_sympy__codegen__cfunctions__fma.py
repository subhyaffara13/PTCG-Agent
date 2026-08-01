
def test_sympy__codegen__cfunctions__fma():
    from sympy.codegen.cfunctions import fma
    assert _test_args(fma(x, y, z))

