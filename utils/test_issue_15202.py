
def test_issue_15202():
    e = (2**x*(2 + 2**(-x)*(-2*2**x + x + 2))/(x + 1))**(x + 1)
    assert limit(e, x, oo) == exp(1)

    e = (log(x, 2)**7 + 10*x*factorial(x) + 5**x) / (factorial(x + 1) + 3*factorial(x) + 10**x)
    assert limit(e, x, oo) == 10

