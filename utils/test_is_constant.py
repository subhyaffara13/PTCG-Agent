
def test_is_constant():
    from sympy.solvers.solvers import checksol
    assert Sum(x, (x, 1, 10)).is_constant() is True
    assert Sum(x, (x, 1, n)).is_constant() is False
    assert Sum(x, (x, 1, n)).is_constant(y) is True
    assert Sum(x, (x, 1, n)).is_constant(n) is False
    assert Sum(x, (x, 1, n)).is_constant(x) is True
    eq = a*cos(x)**2 + a*sin(x)**2 - a
    assert eq.is_constant() is True
    assert eq.subs({x: pi, a: 2}) == eq.subs({x: pi, a: 3}) == 0
    assert x.is_constant() is False
    assert x.is_constant(y) is True
    assert log(x/y).is_constant() is False

    assert checksol(x, x, Sum(x, (x, 1, n))) is False
    assert checksol(x, x, Sum(x, (x, 1, n))) is False
    assert f(1).is_constant
    assert checksol(x, x, f(x)) is False

    assert Pow(x, S.Zero, evaluate=False).is_constant() is True  # == 1
    assert Pow(S.Zero, x, evaluate=False).is_constant() is False  # == 0 or 1
    assert (2**x).is_constant() is False
    assert Pow(S(2), S(3), evaluate=False).is_constant() is True

    z1, z2 = symbols('z1 z2', zero=True)
    assert (z1 + 2*z2).is_constant() is True

    assert meter.is_constant() is True
    assert (3*meter).is_constant() is True
    assert (x*meter).is_constant() is False

