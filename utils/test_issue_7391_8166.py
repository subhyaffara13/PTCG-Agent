
def test_issue_7391_8166():
    f = Function('f')
    # limit should depend on the continuity of the expression at the point passed
    raises(ValueError, lambda: gruntz(f(x), x, 4))
    raises(ValueError, lambda: gruntz(x*f(x)**2/(x**2 + f(x)**4), x, 0))


def test_issue_7391_8166():
    f = Function('f')
    # limit should depend on the continuity of the expression at the point passed
    assert limit(f(x), x, 4) == Limit(f(x), x, 4, dir='+')
    assert limit(x*f(x)**2/(x**2 + f(x)**4), x, 0) == Limit(x*f(x)**2/(x**2 + f(x)**4), x, 0, dir='+')

