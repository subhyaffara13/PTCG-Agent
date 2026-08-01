
def test_issue_15943():
    s = Sum(binomial(n, k)*factorial(n - k), (k, 0, n)).doit().rewrite(gamma)
    assert s == -E*(n + 1)*gamma(n + 1)*lowergamma(n + 1, 1)/gamma(n + 2
        ) + E*gamma(n + 1)
    assert s.simplify() == E*(factorial(n) - lowergamma(n + 1, 1))

