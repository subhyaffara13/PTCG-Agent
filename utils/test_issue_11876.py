
def test_issue_11876():
    assert integrate(sqrt(log(1/x)), (x, 0, 1)) == sqrt(pi)/2

