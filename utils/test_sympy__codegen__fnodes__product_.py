
def test_sympy__codegen__fnodes__product_():
    from sympy.codegen.fnodes import product_
    assert _test_args(product_('arr'))

