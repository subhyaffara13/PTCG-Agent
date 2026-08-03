from typing import Set, Tuple

def test_is_number():
    assert Interval(0, 1).is_number is False
    assert Set().is_number is False


def test_is_number():
    from sympy.abc import x, y, z
    assert Integral(x).is_number is False
    assert Integral(1, x).is_number is False
    assert Integral(1, (x, 1)).is_number is True
    assert Integral(1, (x, 1, 2)).is_number is True
    assert Integral(1, (x, 1, y)).is_number is False
    assert Integral(1, (x, y)).is_number is False
    assert Integral(x, y).is_number is False
    assert Integral(x, (y, 1, x)).is_number is False
    assert Integral(x, (y, 1, 2)).is_number is False
    assert Integral(x, (x, 1, 2)).is_number is True
    # `foo.is_number` should always be equivalent to `not foo.free_symbols`
    # in each of these cases, there are pseudo-free symbols
    i = Integral(x, (y, 1, 1))
    assert i.is_number is False and i.n() == 0
    i = Integral(x, (y, z, z))
    assert i.is_number is False and i.n() == 0
    i = Integral(1, (y, z, z + 2))
    assert i.is_number is False and i.n() == 2.0

    assert Integral(x*y, (x, 1, 2), (y, 1, 3)).is_number is True
    assert Integral(x*y, (x, 1, 2), (y, 1, z)).is_number is False
    assert Integral(x, (x, 1)).is_number is True
    assert Integral(x, (x, 1, Integral(y, (y, 1, 2)))).is_number is True
    assert Integral(Sum(z, (z, 1, 2)), (x, 1, 2)).is_number is True
    # it is possible to get a false negative if the integrand is
    # actually an unsimplified zero, but this is true of is_number in general.
    assert Integral(sin(x)**2 + cos(x)**2 - 1, x).is_number is False
    assert Integral(f(x), (x, 0, 1)).is_number is True


def test_is_number():
    assert Float(3.14).is_number is True
    assert Integer(737).is_number is True
    assert Rational(3, 2).is_number is True
    assert Rational(8).is_number is True
    assert x.is_number is False
    assert (2*x).is_number is False
    assert (x + y).is_number is False
    assert log(2).is_number is True
    assert log(x).is_number is False
    assert (2 + log(2)).is_number is True
    assert (8 + log(2)).is_number is True
    assert (2 + log(x)).is_number is False
    assert (8 + log(2) + x).is_number is False
    assert (1 + x**2/x - x).is_number is True
    assert Tuple(Integer(1)).is_number is False
    assert Add(2, x).is_number is False
    assert Mul(3, 4).is_number is True
    assert Pow(log(2), 2).is_number is True
    assert oo.is_number is True
    g = WildFunction('g')
    assert g.is_number is False
    assert (2*g).is_number is False
    assert (x**2).subs(x, 3).is_number is True

    # test extensibility of .is_number
    # on subinstances of Basic
    class A(Basic):
        pass
    a = A()
    assert a.is_number is False


def test_is_number():
    # is number should not rely on evaluation or assumptions,
    # it should be equivalent to `not foo.free_symbols`
    assert Sum(1, (x, 1, 1)).is_number is True
    assert Sum(1, (x, 1, x)).is_number is False
    assert Sum(0, (x, y, z)).is_number is False
    assert Sum(x, (y, 1, 2)).is_number is False
    assert Sum(x, (y, 1, 1)).is_number is False
    assert Sum(x, (x, 1, 2)).is_number is True
    assert Sum(x*y, (x, 1, 2), (y, 1, 3)).is_number is True

    assert Product(2, (x, 1, 1)).is_number is True
    assert Product(2, (x, 1, y)).is_number is False
    assert Product(0, (x, y, z)).is_number is False
    assert Product(1, (x, y, z)).is_number is False
    assert Product(x, (y, 1, x)).is_number is False
    assert Product(x, (y, 1, 2)).is_number is False
    assert Product(x, (y, 1, 1)).is_number is False
    assert Product(x, (x, 1, 2)).is_number is True

