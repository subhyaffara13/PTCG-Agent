
def test_issue_14103():
    assert Sum(sin(n)**2 + cos(n)**2 - 1, (n, 1, oo)).is_convergent() is S.true
    assert Sum(sin(pi*n), (n, 1, oo)).is_convergent() is S.true

