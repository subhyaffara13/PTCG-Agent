
def test_issue_2725():
    R = Symbol('R')
    eq = sqrt(2)*R*sqrt(1/(R + 1)) + (R + 1)*(sqrt(2)*sqrt(1/(R + 1)) - 1)
    sol = solve(eq, R, set=True)[1]
    assert sol == {(Rational(5, 3) + (Rational(-1, 2) - sqrt(3)*I/2)*(Rational(251, 27) +
        sqrt(111)*I/9)**Rational(1, 3) + 40/(9*((Rational(-1, 2) - sqrt(3)*I/2)*(Rational(251, 27) +
        sqrt(111)*I/9)**Rational(1, 3))),), (Rational(5, 3) + 40/(9*(Rational(251, 27) +
        sqrt(111)*I/9)**Rational(1, 3)) + (Rational(251, 27) + sqrt(111)*I/9)**Rational(1, 3),)}

