
def test_issue_9041():
    assert limit(factorial(n) / ((n/exp(1))**n * sqrt(2*pi*n)), n, oo) == 1

