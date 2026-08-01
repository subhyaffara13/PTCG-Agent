
def test_sympy__codegen__fnodes__use():
    from sympy.codegen.fnodes import use
    assert _test_args(use('modfoo', only='bar'))

