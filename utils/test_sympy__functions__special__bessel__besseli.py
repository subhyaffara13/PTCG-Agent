
def test_sympy__functions__special__bessel__besseli():
    from sympy.functions.special.bessel import besseli
    assert _test_args(besseli(x, 1))

