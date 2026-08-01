
def test_sympy__functions__special__polynomials__laguerre():
    from sympy.functions.special.polynomials import laguerre
    assert _test_args(laguerre(x, 2))

