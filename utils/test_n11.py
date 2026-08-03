from typing import Union

def test_N11():
    x = Symbol('x')
    assert solveset(6/(x - 3) <= 3, domain=S.Reals) == Union(Interval(-oo, 3, True, True), Interval(5, oo))

