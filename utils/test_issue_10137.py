
def test_issue_10137():
    a = Symbol('a', real=True)
    b = Symbol('b', real=True)
    x = Symbol('x', real=True)
    y = Symbol('y', real=True)
    p0 = Piecewise((0, Or(x < a, x > b)), (1, True))
    p1 = Piecewise((0, Or(a > x, b < x)), (1, True))
    assert integrate(p0, (x, y, oo)) == integrate(p1, (x, y, oo))
    p3 = Piecewise((1, And(0 < x, x < a)), (0, True))
    p4 = Piecewise((1, And(a > x, x > 0)), (0, True))
    ip3 = integrate(p3, x)
    assert ip3 == Piecewise(
        (0, x <= 0),
        (x, x <= Max(0, a)),
        (Max(0, a), True))
    ip4 = integrate(p4, x)
    assert ip4 == ip3
    assert p3.integrate((x, 2, 4)) == Min(4, Max(2, a)) - 2
    assert p4.integrate((x, 2, 4)) == Min(4, Max(2, a)) - 2

