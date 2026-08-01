
def test_issue_14313():
    assert Sum(S.Half**floor(n/2), (n, 1, oo)).is_convergent()

