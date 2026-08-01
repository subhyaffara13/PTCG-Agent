
def test_sympy__codegen__cfunctions__log1p():
    from sympy.codegen.cfunctions import log1p
    assert _test_args(log1p(x))

