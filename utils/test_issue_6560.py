
def test_issue_6560():
    e = (5*x**3/4 - x*Rational(3, 4) + (y*(3*x**2/2 - S.Half) +
                             35*x**4/8 - 15*x**2/4 + Rational(3, 8))/(2*(y + 1)))
    assert limit(e, y, oo) == 5*x**3/4 + 3*x**2/4 - 3*x/4 - Rational(1, 4)

