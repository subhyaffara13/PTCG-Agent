
def test_issue_22220():
    e1 = sqrt(30)*atan(sqrt(30)*tan(x/2)/6)/30
    e2 = sqrt(30)*I*(-log(sqrt(2)*tan(x/2) - 2*sqrt(15)*I/5) +
                     +log(sqrt(2)*tan(x/2) + 2*sqrt(15)*I/5))/60

    assert limit(e1, x, -pi) == -sqrt(30)*pi/60
    assert limit(e2, x, -pi) == -sqrt(30)*pi/30

    assert limit(e1, x, -pi, '-') == sqrt(30)*pi/60
    assert limit(e2, x, -pi, '-') == 0

    # test https://github.com/sympy/sympy/issues/22220#issuecomment-972727694
    expr = log(x - I) - log(-x - I)
    expr2 = logcombine(expr, force=True)
    assert limit(expr, x, oo) == limit(expr2, x, oo) == I*pi

    # test https://github.com/sympy/sympy/issues/22220#issuecomment-1077618340
    expr = expr = (-log(tan(x/2) - I) +log(tan(x/2) + I))
    assert limit(expr, x, pi, '+') == 2*I*pi
    assert limit(expr, x, pi, '-') == 0

