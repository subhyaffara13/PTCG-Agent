
def test_issue_12476():
    x0, x1, x2, x3, x4, x5 = symbols('x0 x1 x2 x3 x4 x5')
    eqns = [x0**2 - x0, x0*x1 - x1, x0*x2 - x2, x0*x3 - x3, x0*x4 - x4, x0*x5 - x5,
            x0*x1 - x1, -x0/3 + x1**2 - 2*x2/3, x1*x2 - x1/3 - x2/3 - x3/3,
            x1*x3 - x2/3 - x3/3 - x4/3, x1*x4 - 2*x3/3 - x5/3, x1*x5 - x4, x0*x2 - x2,
            x1*x2 - x1/3 - x2/3 - x3/3, -x0/6 - x1/6 + x2**2 - x2/6 - x3/3 - x4/6,
            -x1/6 + x2*x3 - x2/3 - x3/6 - x4/6 - x5/6, x2*x4 - x2/3 - x3/3 - x4/3,
            x2*x5 - x3, x0*x3 - x3, x1*x3 - x2/3 - x3/3 - x4/3,
            -x1/6 + x2*x3 - x2/3 - x3/6 - x4/6 - x5/6,
            -x0/6 - x1/6 - x2/6 + x3**2 - x3/3 - x4/6, -x1/3 - x2/3 + x3*x4 - x3/3,
            -x2 + x3*x5, x0*x4 - x4, x1*x4 - 2*x3/3 - x5/3, x2*x4 - x2/3 - x3/3 - x4/3,
            -x1/3 - x2/3 + x3*x4 - x3/3, -x0/3 - 2*x2/3 + x4**2, -x1 + x4*x5, x0*x5 - x5,
            x1*x5 - x4, x2*x5 - x3, -x2 + x3*x5, -x1 + x4*x5, -x0 + x5**2, x0 - 1]
    sols = [{x0: 1, x3: Rational(1, 6), x2: Rational(1, 6), x4: Rational(-2, 3), x1: Rational(-2, 3), x5: 1},
            {x0: 1, x3: S.Half, x2: Rational(-1, 2), x4: 0, x1: 0, x5: -1},
            {x0: 1, x3: Rational(-1, 3), x2: Rational(-1, 3), x4: Rational(1, 3), x1: Rational(1, 3), x5: 1},
            {x0: 1, x3: 1, x2: 1, x4: 1, x1: 1, x5: 1},
            {x0: 1, x3: Rational(-1, 3), x2: Rational(1, 3), x4: sqrt(5)/3, x1: -sqrt(5)/3, x5: -1},
            {x0: 1, x3: Rational(-1, 3), x2: Rational(1, 3), x4: -sqrt(5)/3, x1: sqrt(5)/3, x5: -1}]

    assert solve(eqns) == sols

