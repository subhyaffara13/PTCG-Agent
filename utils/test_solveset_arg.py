
def test_solveset_arg():
    assert solveset(arg(x), x, S.Reals)  == Interval.open(0, oo)
    assert solveset(arg(4*x -3), x, S.Reals) == Interval.open(Rational(3, 4), oo)

