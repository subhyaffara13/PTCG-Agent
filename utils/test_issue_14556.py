
def test_issue_14556():
    assert limit(factorial(n + 1)**(1/(n + 1)) - factorial(n)**(1/n), n, oo) == exp(-1)

