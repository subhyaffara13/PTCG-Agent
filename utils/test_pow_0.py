
def test_pow_0():
    assert (x**2).nseries(x, n=5) == x**2
    assert (1/x).nseries(x, n=5) == 1/x
    assert (1/x**2).nseries(x, n=5) == 1/x**2
    assert (x**Rational(2, 3)).nseries(x, n=5) == (x**Rational(2, 3))
    assert (sqrt(x)**3).nseries(x, n=5) == (sqrt(x)**3)

