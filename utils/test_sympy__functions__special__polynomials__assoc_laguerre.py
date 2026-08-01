
def test_sympy__functions__special__polynomials__assoc_laguerre():
    from sympy.functions.special.polynomials import assoc_laguerre
    assert _test_args(assoc_laguerre(x, 0, y))

