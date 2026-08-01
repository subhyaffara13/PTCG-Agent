
def test_T11():
    n, k = symbols('n k', integer=True, positive=True)
    # evaluates to 0
    assert limit(n**x/(x*product((1 + x/k), (k, 1, n))), n, oo) == gamma(x)

