
def test_N9():
    x = Symbol('x')
    assert solveset(abs(x - 1) > 2, domain=S.Reals) == Union(Interval(-oo, -1, False, True),
                                             Interval(3, oo, True))

