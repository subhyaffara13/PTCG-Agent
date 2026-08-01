
def test_sympy__codegen__cfunctions__log2():
    from sympy.codegen.cfunctions import log2
    assert _test_args(log2(x))

