
def test_sympy__codegen__fnodes__isign():
    from sympy.codegen.fnodes import isign
    assert _test_args(isign(1, x))

