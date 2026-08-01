
def test_issue_15847():
    a = Ne(x*(x + y), x**2 + x*y)
    assert simplify(a) == False

