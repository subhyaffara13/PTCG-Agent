
def test_sympy__codegen__cfunctions__log10():
    from sympy.codegen.cfunctions import log10
    assert _test_args(log10(x))

