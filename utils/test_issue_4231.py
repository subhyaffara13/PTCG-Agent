
def test_issue_4231():
    f = (1 + 2*x + sqrt(x + log(x))*(1 + 3*x) + x**2)/(x*(x + sqrt(x + log(x)))*sqrt(x + log(x)))
    assert integrate(f, x) == 2*sqrt(x + log(x)) + 2*log(x + sqrt(x + log(x)))

