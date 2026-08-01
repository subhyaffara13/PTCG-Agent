
def test_sympy__functions__special__bessel__marcumq():
    from sympy.functions.special.bessel import marcumq
    assert _test_args(marcumq(x, y, z))

