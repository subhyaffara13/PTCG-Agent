
def test_sympy__codegen__fnodes__sum_():
    from sympy.codegen.fnodes import sum_
    assert _test_args(sum_('arr'))

