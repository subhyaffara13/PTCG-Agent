
def test_issue_20777():
    assert Sum(exp(x*sin(n/m)), (n, 1, m)).doit() == Sum(exp(x*sin(n/m)), (n, 1, m))

