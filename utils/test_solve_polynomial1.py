
def test_solve_polynomial1():
    assert solve(3*x - 2, x) == [Rational(2, 3)]
    assert solve(Eq(3*x, 2), x) == [Rational(2, 3)]

    assert set(solve(x**2 - 1, x)) == {-S.One, S.One}
    assert set(solve(Eq(x**2, 1), x)) == {-S.One, S.One}

    assert solve(x - y**3, x) == [y**3]
    rx = root(x, 3)
    assert solve(x - y**3, y) == [
        rx, -rx/2 - sqrt(3)*I*rx/2, -rx/2 +  sqrt(3)*I*rx/2]
    a11, a12, a21, a22, b1, b2 = symbols('a11,a12,a21,a22,b1,b2')

    assert solve([a11*x + a12*y - b1, a21*x + a22*y - b2], x, y) == \
        {
            x: (a22*b1 - a12*b2)/(a11*a22 - a12*a21),
            y: (a11*b2 - a21*b1)/(a11*a22 - a12*a21),
        }

    solution = {x: S.Zero, y: S.Zero}

    assert solve((x - y, x + y), x, y ) == solution
    assert solve((x - y, x + y), (x, y)) == solution
    assert solve((x - y, x + y), [x, y]) == solution

    assert set(solve(x**3 - 15*x - 4, x)) == {
        -2 + 3**S.Half,
        S(4),
        -2 - 3**S.Half
    }

    assert set(solve((x**2 - 1)**2 - a, x)) == \
        {sqrt(1 + sqrt(a)), -sqrt(1 + sqrt(a)),
             sqrt(1 - sqrt(a)), -sqrt(1 - sqrt(a))}

