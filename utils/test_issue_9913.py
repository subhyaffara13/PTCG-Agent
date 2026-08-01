
def test_issue_9913():
    assert solveset(2*x + 1/(x - 10)**2, x, S.Reals) == \
        FiniteSet(-(3*sqrt(24081)/4 + Rational(4027, 4))**Rational(1, 3)/3 - 100/
                (3*(3*sqrt(24081)/4 + Rational(4027, 4))**Rational(1, 3)) + Rational(20, 3))

