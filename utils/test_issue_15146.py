
def test_issue_15146():
    e = (x/2) * (-2*x**3 - 2*(x**3 - 1) * x**2 * digamma(x**3 + 1) + \
        2*(x**3 - 1) * x**2 * digamma(x**3 + x + 1) + x + 3)
    assert limit(e, x, oo) == S(1)/3

