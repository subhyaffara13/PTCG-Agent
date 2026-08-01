
def test_sympy__functions__special__bessel__besselk():
    from sympy.functions.special.bessel import besselk
    assert _test_args(besselk(x, 1))

