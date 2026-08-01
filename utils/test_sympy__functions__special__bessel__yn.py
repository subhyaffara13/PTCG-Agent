
def test_sympy__functions__special__bessel__yn():
    from sympy.functions.special.bessel import yn
    assert _test_args(yn(0, x))

