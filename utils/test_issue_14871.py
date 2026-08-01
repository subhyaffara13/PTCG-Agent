
def test_issue_14871():
    assert Sum((Rational(1, 10))**n*rf(0, n)/factorial(n), (n, 0, oo)).rewrite(factorial).doit() == 1

