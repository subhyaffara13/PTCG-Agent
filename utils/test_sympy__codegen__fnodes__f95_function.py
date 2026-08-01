
def test_sympy__codegen__fnodes__F95Function():
    from sympy.codegen.fnodes import F95Function
    assert _test_args(F95Function('f'))

