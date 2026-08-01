
def test_issue_18992():
    assert limit(n/(factorial(n)**(1/n)), n, oo) == exp(1)

