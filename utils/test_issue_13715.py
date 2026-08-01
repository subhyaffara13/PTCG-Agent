
def test_issue_13715():
    n = Symbol('n')
    p = Symbol('p', zero=True)
    assert limit(n + p, n, 0) == 0

