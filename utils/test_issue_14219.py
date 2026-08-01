
def test_issue_14219():
    A = diag(0, 2, -3)
    res = diag(1, 15, -20)
    assert Sum(A**n, (n, 0, 3)).doit() == res

