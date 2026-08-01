
def test_issue_17565():
    eq = Ge(2*(x - 2)**2/(3*(x + 1)**(Integer(1)/3)) + 2*(x - 2)*(x + 1)**(Integer(2)/3), 0)
    res = Union(Interval.Lopen(-1, -Rational(1, 4)), Interval(2, oo))
    assert solveset(eq, x, S.Reals) == res

