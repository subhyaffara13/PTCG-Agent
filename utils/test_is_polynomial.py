
def test_is_polynomial():
    k = Symbol('k', nonnegative=True, integer=True)

    assert Rational(2).is_polynomial(x, y, z) is True
    assert (S.Pi).is_polynomial(x, y, z) is True

    assert x.is_polynomial(x) is True
    assert x.is_polynomial(y) is True

    assert (x**2).is_polynomial(x) is True
    assert (x**2).is_polynomial(y) is True

    assert (x**(-2)).is_polynomial(x) is False
    assert (x**(-2)).is_polynomial(y) is True

    assert (2**x).is_polynomial(x) is False
    assert (2**x).is_polynomial(y) is True

    assert (x**k).is_polynomial(x) is False
    assert (x**k).is_polynomial(k) is False
    assert (x**x).is_polynomial(x) is False
    assert (k**k).is_polynomial(k) is False
    assert (k**x).is_polynomial(k) is False

    assert (x**(-k)).is_polynomial(x) is False
    assert ((2*x)**k).is_polynomial(x) is False

    assert (x**2 + 3*x - 8).is_polynomial(x) is True
    assert (x**2 + 3*x - 8).is_polynomial(y) is True

    assert (x**2 + 3*x - 8).is_polynomial() is True

    assert sqrt(x).is_polynomial(x) is False
    assert (sqrt(x)**3).is_polynomial(x) is False

    assert (x**2 + 3*x*sqrt(y) - 8).is_polynomial(x) is True
    assert (x**2 + 3*x*sqrt(y) - 8).is_polynomial(y) is False

    assert ((x**2)*(y**2) + x*(y**2) + y*x + exp(2)).is_polynomial() is True
    assert ((x**2)*(y**2) + x*(y**2) + y*x + exp(x)).is_polynomial() is False

    assert (
        (x**2)*(y**2) + x*(y**2) + y*x + exp(2)).is_polynomial(x, y) is True
    assert (
        (x**2)*(y**2) + x*(y**2) + y*x + exp(x)).is_polynomial(x, y) is False

    assert (1/f(x) + 1).is_polynomial(f(x)) is False

