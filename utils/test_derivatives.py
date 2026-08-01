
def test_derivatives():
    from sympy.core.function import Derivative
    assert zeta(x, a).diff(x) == Derivative(zeta(x, a), x)
    assert zeta(x, a).diff(a) == -x*zeta(x + 1, a)
    assert lerchphi(
        z, s, a).diff(z) == (lerchphi(z, s - 1, a) - a*lerchphi(z, s, a))/z
    assert lerchphi(z, s, a).diff(a) == -s*lerchphi(z, s + 1, a)
    assert polylog(s, z).diff(z) == polylog(s - 1, z)/z

    b = randcplx()
    c = randcplx()
    assert td(zeta(b, x), x)
    assert td(polylog(b, z), z)
    assert td(lerchphi(c, b, x), x)
    assert td(lerchphi(x, b, c), x)
    raises(ArgumentIndexError, lambda: lerchphi(c, b, x).fdiff(2))
    raises(ArgumentIndexError, lambda: lerchphi(c, b, x).fdiff(4))
    raises(ArgumentIndexError, lambda: polylog(b, z).fdiff(1))
    raises(ArgumentIndexError, lambda: polylog(b, z).fdiff(3))

