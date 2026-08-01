
def test_pow_1():
    assert ((1 + x)**2).nseries(x, n=5) == x**2 + 2*x + 1

    # https://github.com/sympy/sympy/issues/21075
    assert ((sqrt(x) + 1)**2).nseries(x) == 2*sqrt(x) + x + 1
    assert ((sqrt(x) + cbrt(x))**2).nseries(x) == 2*x**Rational(5, 6)\
        + x**Rational(2, 3) + x

