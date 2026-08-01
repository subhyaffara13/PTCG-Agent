
def test_sympy__codegen__cfunctions__hypot():
    from sympy.codegen.cfunctions import hypot
    assert _test_args(hypot(x, y))

