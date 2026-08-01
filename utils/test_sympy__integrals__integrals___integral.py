
def test_sympy__integrals__integrals__Integral():
    from sympy.integrals.integrals import Integral
    assert _test_args(Integral(2, (x, 0, 1)))

