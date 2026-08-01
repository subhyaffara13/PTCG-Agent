
def test_basic1():
    assert limit(x, x, oo) is oo
    assert limit(x, x, -oo) is -oo
    assert limit(-x, x, oo) is -oo
    assert limit(x**2, x, -oo) is oo
    assert limit(-x**2, x, oo) is -oo
    assert limit(x*log(x), x, 0, dir="+") == 0
    assert limit(1/x, x, oo) == 0
    assert limit(exp(x), x, oo) is oo
    assert limit(-exp(x), x, oo) is -oo
    assert limit(exp(x)/x, x, oo) is oo
    assert limit(1/x - exp(-x), x, oo) == 0
    assert limit(x + 1/x, x, oo) is oo
    assert limit(x - x**2, x, oo) is -oo
    assert limit((1 + x)**(1 + sqrt(2)), x, 0) == 1
    assert limit((1 + x)**oo, x, 0) == Limit((x + 1)**oo, x, 0)
    assert limit((1 + x)**oo, x, 0, dir='-') == Limit((x + 1)**oo, x, 0, dir='-')
    assert limit((1 + x + y)**oo, x, 0, dir='-') == Limit((1 + x + y)**oo, x, 0, dir='-')
    assert limit(y/x/log(x), x, 0) == -oo*sign(y)
    assert limit(cos(x + y)/x, x, 0) == sign(cos(y))*oo
    assert limit(gamma(1/x + 3), x, oo) == 2
    assert limit(S.NaN, x, -oo) is S.NaN
    assert limit(Order(2)*x, x, S.NaN) is S.NaN
    assert limit(1/(x - 1), x, 1, dir="+") is oo
    assert limit(1/(x - 1), x, 1, dir="-") is -oo
    assert limit(1/(5 - x)**3, x, 5, dir="+") is -oo
    assert limit(1/(5 - x)**3, x, 5, dir="-") is oo
    assert limit(1/sin(x), x, pi, dir="+") is -oo
    assert limit(1/sin(x), x, pi, dir="-") is oo
    assert limit(1/cos(x), x, pi/2, dir="+") is -oo
    assert limit(1/cos(x), x, pi/2, dir="-") is oo
    assert limit(1/tan(x**3), x, (2*pi)**Rational(1, 3), dir="+") is oo
    assert limit(1/tan(x**3), x, (2*pi)**Rational(1, 3), dir="-") is -oo
    assert limit(1/cot(x)**3, x, (pi*Rational(3, 2)), dir="+") is -oo
    assert limit(1/cot(x)**3, x, (pi*Rational(3, 2)), dir="-") is oo
    assert limit(tan(x), x, oo) == AccumBounds(S.NegativeInfinity, S.Infinity)
    assert limit(cot(x), x, oo) == AccumBounds(S.NegativeInfinity, S.Infinity)
    assert limit(sec(x), x, oo) == AccumBounds(S.NegativeInfinity, S.Infinity)
    assert limit(csc(x), x, oo) == AccumBounds(S.NegativeInfinity, S.Infinity)

    # test bi-directional limits
    assert limit(sin(x)/x, x, 0, dir="+-") == 1
    assert limit(x**2, x, 0, dir="+-") == 0
    assert limit(1/x**2, x, 0, dir="+-") is oo

    # test failing bi-directional limits
    assert limit(1/x, x, 0, dir="+-") is zoo
    # approaching 0
    # from dir="+"
    assert limit(1 + 1/x, x, 0) is oo
    # from dir='-'
    # Add
    assert limit(1 + 1/x, x, 0, dir='-') is -oo
    # Pow
    assert limit(x**(-2), x, 0, dir='-') is oo
    assert limit(x**(-3), x, 0, dir='-') is -oo
    assert limit(1/sqrt(x), x, 0, dir='-') == (-oo)*I
    assert limit(x**2, x, 0, dir='-') == 0
    assert limit(sqrt(x), x, 0, dir='-') == 0
    assert limit(x**-pi, x, 0, dir='-') == -oo*(-1)**(1 - pi)
    assert limit((1 + cos(x))**oo, x, 0) == Limit((cos(x) + 1)**oo, x, 0)

    # test pull request 22491
    assert limit(1/asin(x), x, 0, dir = '+') == oo
    assert limit(1/asin(x), x, 0, dir = '-') == -oo
    assert limit(1/sinh(x), x, 0, dir = '+') == oo
    assert limit(1/sinh(x), x, 0, dir = '-') == -oo
    assert limit(log(1/x) + 1/sin(x), x, 0, dir = '+') == oo
    assert limit(log(1/x) + 1/x, x, 0, dir = '+') == oo


def test_basic1():
    assert residue(1/x, x, 0) == 1
    assert residue(-2/x, x, 0) == -2
    assert residue(81/x, x, 0) == 81
    assert residue(1/x**2, x, 0) == 0
    assert residue(0, x, 0) == 0
    assert residue(5, x, 0) == 0
    assert residue(x, x, 0) == 0
    assert residue(x**2, x, 0) == 0

