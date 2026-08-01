
def test_N14():
    x = Symbol('x')
    # Gives 'Union(Interval(Integer(0), Mul(Rational(1, 2), pi), false, true),
    #        Interval(Mul(Rational(1, 2), pi), Mul(Integer(2), pi), true, false))'
    # which is not the correct answer, but the provided also seems wrong.
    assert solveset(sin(x) < 1, x, domain=S.Reals) == Union(Interval(-oo, pi/2, True, True),
                                         Interval(pi/2, oo, True, True))

