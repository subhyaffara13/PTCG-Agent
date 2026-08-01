
def test_solve_for_functions_derivatives():
    t = Symbol('t')
    x = Function('x')(t)
    y = Function('y')(t)
    a11, a12, a21, a22, b1, b2 = symbols('a11,a12,a21,a22,b1,b2')

    soln = solve([a11*x + a12*y - b1, a21*x + a22*y - b2], x, y)
    assert soln == {
        x: (a22*b1 - a12*b2)/(a11*a22 - a12*a21),
        y: (a11*b2 - a21*b1)/(a11*a22 - a12*a21),
    }

    assert solve(x - 1, x) == [1]
    assert solve(3*x - 2, x) == [Rational(2, 3)]

    soln = solve([a11*x.diff(t) + a12*y.diff(t) - b1, a21*x.diff(t) +
            a22*y.diff(t) - b2], x.diff(t), y.diff(t))
    assert soln == { y.diff(t): (a11*b2 - a21*b1)/(a11*a22 - a12*a21),
            x.diff(t): (a22*b1 - a12*b2)/(a11*a22 - a12*a21) }

    assert solve(x.diff(t) - 1, x.diff(t)) == [1]
    assert solve(3*x.diff(t) - 2, x.diff(t)) == [Rational(2, 3)]

    eqns = {3*x - 1, 2*y - 4}
    assert solve(eqns, {x, y}) == { x: Rational(1, 3), y: 2 }
    x = Symbol('x')
    f = Function('f')
    F = x**2 + f(x)**2 - 4*x - 1
    assert solve(F.diff(x), diff(f(x), x)) == [(-x + 2)/f(x)]

    # Mixed cased with a Symbol and a Function
    x = Symbol('x')
    y = Function('y')(t)

    soln = solve([a11*x + a12*y.diff(t) - b1, a21*x +
            a22*y.diff(t) - b2], x, y.diff(t))
    assert soln == { y.diff(t): (a11*b2 - a21*b1)/(a11*a22 - a12*a21),
            x: (a22*b1 - a12*b2)/(a11*a22 - a12*a21) }

    # issue 13263
    x = Symbol('x')
    f = Function('f')
    soln = solve([f(x).diff(x) + f(x).diff(x, 2) - 1, f(x).diff(x) - f(x).diff(x, 2)],
            f(x).diff(x), f(x).diff(x, 2))
    assert soln == { f(x).diff(x, 2): S(1)/2, f(x).diff(x): S(1)/2 }

    soln = solve([f(x).diff(x, 2) + f(x).diff(x, 3) - 1, 1 - f(x).diff(x, 2) -
            f(x).diff(x, 3), 1 - f(x).diff(x,3)], f(x).diff(x, 2), f(x).diff(x, 3))
    assert soln == { f(x).diff(x, 2): 0, f(x).diff(x, 3): 1 }

