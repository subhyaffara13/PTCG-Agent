from typing import Union

def test_issue_10113():
    f = x**2/(x**2 - 4)
    assert imageset(x, f, S.Reals) == Union(Interval(-oo, 0), Interval(1, oo, True, True))
    assert imageset(x, f, Interval(-2, 2)) == Interval(-oo, 0)
    assert imageset(x, f, Interval(-2, 3)) == Union(Interval(-oo, 0), Interval(Rational(9, 5), oo))

