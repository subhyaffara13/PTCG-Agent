
def test_issue_11879():
    assert simplify(limit(((x+y)**n-x**n)/y, y, 0)) == n*x**(n-1)

