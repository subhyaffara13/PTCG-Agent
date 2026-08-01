
def test_abs1():
    a = Symbol("a", real=True)
    b = Symbol("b", real=True)
    assert abs(a) == Abs(a)
    assert abs(-a) == abs(a)
    assert abs(a + I*b) == sqrt(a**2 + b**2)


def test_abs1():
    assert Rational(1, 6) != Rational(-1, 6)
    assert abs(Rational(1, 6)) == abs(Rational(-1, 6))

