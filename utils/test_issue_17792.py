
def test_issue_17792():
    assert limit(factorial(n)/sqrt(n)*(exp(1)/n)**n, n, oo) == sqrt(2)*sqrt(pi)

