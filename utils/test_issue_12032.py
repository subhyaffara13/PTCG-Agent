
def test_issue_12032():
    sol = FiniteSet(-sqrt(-2/(3*(Rational(1, 16) + sqrt(849)/144)**(Rational(1, 3))) +
                          2*(Rational(1, 16) + sqrt(849)/144)**(Rational(1, 3)))/2 +
                    sqrt(Abs(-2*(Rational(1, 16) + sqrt(849)/144)**(Rational(1, 3)) +
                             2/(3*(Rational(1, 16) + sqrt(849)/144)**(Rational(1, 3))) +
                             2/sqrt(-2/(3*(Rational(1, 16) + sqrt(849)/144)**(Rational(1, 3))) +
                                    2*(Rational(1, 16) + sqrt(849)/144)**(Rational(1, 3)))))/2,
                    -sqrt(Abs(-2*(Rational(1, 16) + sqrt(849)/144)**(Rational(1, 3)) +
                              2/(3*(Rational(1, 16) + sqrt(849)/144)**(Rational(1, 3))) +
                              2/sqrt(-2/(3*(Rational(1, 16) + sqrt(849)/144)**(Rational(1, 3))) +
                                     2*(Rational(1, 16) + sqrt(849)/144)**(Rational(1, 3)))))/2 -
                    sqrt(-2/(3*(Rational(1, 16) + sqrt(849)/144)**(Rational(1, 3))) +
                         2*(Rational(1, 16) + sqrt(849)/144)**(Rational(1, 3)))/2,
                    sqrt(-2/(3*(Rational(1, 16) + sqrt(849)/144)**(Rational(1, 3))) +
                         2*(Rational(1, 16) + sqrt(849)/144)**(Rational(1, 3)))/2 -
                    I*sqrt(Abs(-2/sqrt(-2/(3*(Rational(1, 16) + sqrt(849)/144)**(Rational(1, 3))) +
                                       2*(Rational(1, 16) + sqrt(849)/144)**(Rational(1, 3))) -
                               2*(Rational(1, 16) + sqrt(849)/144)**(Rational(1, 3)) +
                               2/(3*(Rational(1, 16) + sqrt(849)/144)**(Rational(1, 3)))))/2,
                    sqrt(-2/(3*(Rational(1, 16) + sqrt(849)/144)**(Rational(1, 3))) +
                         2*(Rational(1, 16) + sqrt(849)/144)**(Rational(1, 3)))/2 +
                    I*sqrt(Abs(-2/sqrt(-2/(3*(Rational(1, 16) + sqrt(849)/144)**(Rational(1, 3))) +
                                       2*(Rational(1, 16) + sqrt(849)/144)**(Rational(1, 3))) -
                               2*(Rational(1, 16) + sqrt(849)/144)**(Rational(1, 3)) +
                               2/(3*(Rational(1, 16) + sqrt(849)/144)**(Rational(1,3)))))/2)
    assert solveset(x**4 + x - 1, x) == sol

