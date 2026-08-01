
def test_sympy__functions__special__bessel__besselj():
    from sympy.functions.special.bessel import besselj
    assert _test_args(besselj(x, 1))

