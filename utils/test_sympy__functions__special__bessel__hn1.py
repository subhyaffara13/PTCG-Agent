
def test_sympy__functions__special__bessel__hn1():
    from sympy.functions.special.bessel import hn1
    assert _test_args(hn1(0, x))

