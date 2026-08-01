
def test_issue_17431():
    assert limit(((n + 1) + 1) / (((n + 1) + 2) * factorial(n + 1)) *
                 (n + 2) * factorial(n) / (n + 1), n, oo) == 0
    assert limit((n + 2)**2*factorial(n)/((n + 1)*(n + 3)*factorial(n + 1))
                 , n, oo) == 0
    assert limit((n + 1) * factorial(n) / (n * factorial(n + 1)), n, oo) == 0

