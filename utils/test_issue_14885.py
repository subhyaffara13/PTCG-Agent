
def test_issue_14885():
    assert series(x**Rational(-3, 2)*exp(x), x, 0) == (x**Rational(-3, 2) + 1/sqrt(x) +
        sqrt(x)/2 + x**Rational(3, 2)/6 + x**Rational(5, 2)/24 + x**Rational(7, 2)/120 +
        x**Rational(9, 2)/720 + x**Rational(11, 2)/5040 + O(x**6))

