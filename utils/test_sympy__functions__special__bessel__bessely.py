
def test_sympy__functions__special__bessel__bessely():
    from sympy.functions.special.bessel import bessely
    assert _test_args(bessely(x, 1))

