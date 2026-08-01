
def test_apart():
    assert apart(1) == 1
    assert apart(1, x) == 1

    f, g = (x**2 + 1)/(x + 1), 2/(x + 1) + x - 1

    assert apart(f, full=False) == g
    assert apart(f, full=True) == g

    f, g = 1/(x + 2)/(x + 1), 1/(1 + x) - 1/(2 + x)

    assert apart(f, full=False) == g
    assert apart(f, full=True) == g

    f, g = 1/(x + 1)/(x + 5), -1/(5 + x)/4 + 1/(1 + x)/4

    assert apart(f, full=False) == g
    assert apart(f, full=True) == g

    assert apart((E*x + 2)/(x - pi)*(x - 1), x) == \
        2 - E + E*pi + E*x + (E*pi + 2)*(pi - 1)/(x - pi)

    assert apart(Eq((x**2 + 1)/(x + 1), x), x) == Eq(x - 1 + 2/(x + 1), x)

    assert apart(x/2, y) == x/2

    f, g = (x+y)/(2*x - y), Rational(3, 2)*y/(2*x - y) + S.Half

    assert apart(f, x, full=False) == g
    assert apart(f, x, full=True) == g

    f, g = (x+y)/(2*x - y), 3*x/(2*x - y) - 1

    assert apart(f, y, full=False) == g
    assert apart(f, y, full=True) == g

    raises(NotImplementedError, lambda: apart(1/(x + 1)/(y + 2)))

