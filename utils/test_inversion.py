
def test_inversion():
    R, x = ring('x', QQ)
    p = 2 + x + 2*x**2
    n = 5
    p1 = rs_series_inversion(p, x, n)
    assert rs_trunc(p*p1, x, n) == 1
    R, x, y = ring('x, y', QQ)
    p = 2 + x + 2*x**2 + y*x + x**2*y
    p1 = rs_series_inversion(p, x, n)
    assert rs_trunc(p*p1, x, n) == 1

    R, x, y = ring('x, y', QQ)
    p = 1 + x + y
    raises(NotImplementedError, lambda: rs_series_inversion(p, x, 4))
    p = R.zero
    raises(ZeroDivisionError, lambda: rs_series_inversion(p, x, 3))

    R, x = ring('x', ZZ)
    p = 2 + x
    raises(ValueError, lambda: rs_series_inversion(p, x, 3))


def test_inversion():
    from sympy.functions.special.bessel import besselj
    from sympy.functions.special.delta_functions import Heaviside

    def inv(f):
        return piecewise_fold(meijerint_inversion(f, s, t))
    assert inv(1/(s**2 + 1)) == sin(t)*Heaviside(t)
    assert inv(s/(s**2 + 1)) == cos(t)*Heaviside(t)
    assert inv(exp(-s)/s) == Heaviside(t - 1)
    assert inv(1/sqrt(1 + s**2)) == besselj(0, t)*Heaviside(t)

    # Test some antcedents checking.
    assert meijerint_inversion(sqrt(s)/sqrt(1 + s**2), s, t) is None
    assert inv(exp(s**2)) is None
    assert meijerint_inversion(exp(-s**2), s, t) is None

