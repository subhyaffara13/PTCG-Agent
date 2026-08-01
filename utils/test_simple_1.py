
def test_simple_1():
    assert x.nseries(x, n=5) == x
    assert y.nseries(x, n=5) == y
    assert (1/(x*y)).nseries(y, n=5) == 1/(x*y)
    assert Rational(3, 4).nseries(x, n=5) == Rational(3, 4)
    assert x.nseries() == x


def test_simple_1():
    o = Rational(0)
    assert Order(2*x) == Order(x)
    assert Order(x)*3 == Order(x)
    assert -28*Order(x) == Order(x)
    assert Order(Order(x)) == Order(x)
    assert Order(Order(x), y) == Order(Order(x), x, y)
    assert Order(-23) == Order(1)
    assert Order(exp(x)) == Order(1, x)
    assert Order(exp(1/x)).expr == exp(1/x)
    assert Order(x*exp(1/x)).expr == x*exp(1/x)
    assert Order(x**(o/3)).expr == x**(o/3)
    assert Order(x**(o*Rational(5, 3))).expr == x**(o*Rational(5, 3))
    assert Order(x**2 + x + y, x) == O(1, x)
    assert Order(x**2 + x + y, y) == O(1, y)
    raises(ValueError, lambda: Order(exp(x), x, x))
    raises(TypeError, lambda: Order(x, 2 - x))

