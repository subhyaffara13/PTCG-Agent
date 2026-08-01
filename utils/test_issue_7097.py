
def test_issue_7097():
    assert sum(x**n/n for n in range(1, 401)) == summation(x**n/n, (n, 1, 400))

