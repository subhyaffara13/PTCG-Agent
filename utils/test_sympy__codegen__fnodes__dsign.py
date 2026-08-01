
def test_sympy__codegen__fnodes__dsign():
    from sympy.codegen.fnodes import dsign
    assert _test_args(dsign(1, x))

