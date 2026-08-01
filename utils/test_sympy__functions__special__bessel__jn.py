
def test_sympy__functions__special__bessel__jn():
    from sympy.functions.special.bessel import jn
    assert _test_args(jn(0, x))

