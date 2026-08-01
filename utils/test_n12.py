
def test_N12():
    x = Symbol('x')
    assert solveset(sqrt(x) < 2, domain=S.Reals) == Interval(0, 4, False, True)

