
def test_sympy__codegen__fnodes__cmplx():
    from sympy.codegen.fnodes import cmplx
    assert _test_args(cmplx(x, y))

