
def test_issue_18008():
    y = x*(1 + x*(1 - x))/((1 + x*(1 - x)) - (1 - x)*(1 - x))
    assert y.series(x, oo, n=4) == -9/(32*x**3) - 3/(16*x**2) - 1/(8*x) + S(1)/4 + x/2 + \
        O(x**(-4), (x, oo))

