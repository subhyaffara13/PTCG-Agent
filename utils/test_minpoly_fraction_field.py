
def test_minpoly_fraction_field():
    assert minimal_polynomial(1/x, y) == -x*y + 1
    assert minimal_polynomial(1 / (x + 1), y) == (x + 1)*y - 1

    assert minimal_polynomial(sqrt(x), y) == y**2 - x
    assert minimal_polynomial(sqrt(x + 1), y) == y**2 - x - 1
    assert minimal_polynomial(sqrt(x) / x, y) == x*y**2 - 1
    assert minimal_polynomial(sqrt(2) * sqrt(x), y) == y**2 - 2 * x
    assert minimal_polynomial(sqrt(2) + sqrt(x), y) == \
        y**4 + (-2*x - 4)*y**2 + x**2 - 4*x + 4

    assert minimal_polynomial(x**Rational(1,3), y) == y**3 - x
    assert minimal_polynomial(x**Rational(1,3) + sqrt(x), y) == \
        y**6 - 3*x*y**4 - 2*x*y**3 + 3*x**2*y**2 - 6*x**2*y - x**3 + x**2

    assert minimal_polynomial(sqrt(x) / z, y) == z**2*y**2 - x
    assert minimal_polynomial(sqrt(x) / (z + 1), y) == (z**2 + 2*z + 1)*y**2 - x

    assert minimal_polynomial(1/x, y, polys=True) == Poly(-x*y + 1, y, domain='ZZ(x)')
    assert minimal_polynomial(1 / (x + 1), y, polys=True) == \
        Poly((x + 1)*y - 1, y, domain='ZZ(x)')
    assert minimal_polynomial(sqrt(x), y, polys=True) == Poly(y**2 - x, y, domain='ZZ(x)')
    assert minimal_polynomial(sqrt(x) / z, y, polys=True) == \
        Poly(z**2*y**2 - x, y, domain='ZZ(x, z)')

    # this is (sqrt(1 + x**3)/x).integrate(x).diff(x) - sqrt(1 + x**3)/x
    a = sqrt(x)/sqrt(1 + x**(-3)) - sqrt(x**3 + 1)/x + 1/(x**Rational(5, 2)* \
        (1 + x**(-3))**Rational(3, 2)) + 1/(x**Rational(11, 2)*(1 + x**(-3))**Rational(3, 2))

    assert minimal_polynomial(a, y) == y

    raises(NotAlgebraic, lambda: minimal_polynomial(exp(x), y))
    raises(GeneratorsError, lambda: minimal_polynomial(sqrt(x), x))
    raises(GeneratorsError, lambda: minimal_polynomial(sqrt(x) - y, x))
    raises(NotImplementedError, lambda: minimal_polynomial(sqrt(x), y, compose=False))

