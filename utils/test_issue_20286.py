
def test_issue_20286():
    n, p = symbols('n p')
    B = Binomial('B', n, p)
    k = Dummy('k', integer = True)
    eq = Sum(Piecewise((-p**k*(1 - p)**(-k + n)*log(p**k*(1 - p)**(-k + n)*binomial(n, k))*binomial(n, k), (k >= 0) & (k <= n)), (nan, True)), (k, 0, n))
    assert eq.dummy_eq(H(B))

