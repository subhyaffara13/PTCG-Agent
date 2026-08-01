
def test_division():
    v = Matrix(1, 2, [x, y])
    assert v/z == Matrix(1, 2, [x/z, y/z])


def test_division():
    v = Matrix(1, 2, [x, y])
    assert v/z == Matrix(1, 2, [x/z, y/z])


def test_division():
    a, b, c = symbols('a b c', commutative=True)
    x, y, z = symbols('x y z', commutative=True)

    assert (1/a).subs(a, c) == 1/c
    assert (1/a**2).subs(a, c) == 1/c**2
    assert (1/a**2).subs(a, -2) == Rational(1, 4)
    assert (-(1/a**2)).subs(a, -2) == Rational(-1, 4)

    assert (1/x).subs(x, z) == 1/z
    assert (1/x**2).subs(x, z) == 1/z**2
    assert (1/x**2).subs(x, -2) == Rational(1, 4)
    assert (-(1/x**2)).subs(x, -2) == Rational(-1, 4)

    #issue 5360
    assert (1/x).subs(x, 0) == 1/S.Zero

