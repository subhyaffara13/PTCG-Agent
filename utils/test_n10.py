
def test_N10():
    x = Symbol('x')
    p = (x - 1)*(x - 2)*(x - 3)*(x - 4)*(x - 5)
    assert solveset(expand(p) < 0, domain=S.Reals) == Union(Interval(-oo, 1, True, True),
                                            Interval(2, 3, True, True),
                                            Interval(4, 5, True, True))

