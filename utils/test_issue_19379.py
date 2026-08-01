
def test_issue_19379():
    assert Sum(factorial(n)/factorial(n + 2), (n, 1, oo)).is_convergent() is S.true

