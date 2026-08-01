
def test_issue_3505():
    e = sin(x)**(-4)*(sqrt(cos(x))*sin(x)**2 -
        cos(x)**Rational(1, 3)*sin(x)**2)
    assert e.nseries(x, n=9) == Rational(-1, 12) - 7*x**2/288 - \
        43*x**4/10368 - 1123*x**6/2488320 + 377*x**8/29859840 + O(x**9)

