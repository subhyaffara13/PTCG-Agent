
def test_issue_8016():
    k = Symbol('k', integer=True)
    n, m = symbols('n, m', integer=True, positive=True)
    s = Sum(binomial(m, k)*binomial(m, n - k)*(-1)**k, (k, 0, n))
    assert s.doit().simplify() == \
        cos(pi*n/2)*gamma(m + 1)/gamma(n/2 + 1)/gamma(m - n/2 + 1)

