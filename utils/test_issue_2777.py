
def test_issue_2777():
    # the equations represent two circles
    x, y = symbols('x y', real=True)
    e1, e2 = sqrt(x**2 + y**2) - 10, sqrt(y**2 + (-x + 10)**2) - 3
    a, b = Rational(191, 20), 3*sqrt(391)/20
    ans = [(a, -b), (a, b)]
    assert solve((e1, e2), (x, y)) == ans
    assert solve((e1, e2/(x - a)), (x, y)) == []
    # make the 2nd circle's radius be -3
    e2 += 6
    assert solve((e1, e2), (x, y)) == []
    assert solve((e1, e2), (x, y), check=False) == ans


def test_issue_2777():
    # the equations represent two circles
    x, y = symbols('x y', real=True)
    e1, e2 = sqrt(x**2 + y**2) - 10, sqrt(y**2 + (-x + 10)**2) - 3
    a, b = Rational(191, 20), 3*sqrt(391)/20
    ans = {(a, -b), (a, b)}
    assert nonlinsolve((e1, e2), (x, y)) == ans
    assert nonlinsolve((e1, e2/(x - a)), (x, y)) == S.EmptySet
    # make the 2nd circle's radius be -3
    e2 += 6
    assert nonlinsolve((e1, e2), (x, y)) == S.EmptySet

