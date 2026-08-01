
def test_issue_6343():
    eq = -3*x**2/2 - x*Rational(45, 4) + Rational(33, 2) > 0
    assert reduce_inequalities(eq) == \
        And(x < Rational(-15, 4) + sqrt(401)/4, -sqrt(401)/4 - Rational(15, 4) < x)

