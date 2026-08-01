
def test_issue_22628():
    assert nonlinsolve([h - 1, k - 1, f - 2, f - 4, -2*k], h, k, f) == S.EmptySet
    assert nonlinsolve([x**3 - 1, x + y, x**2 - 4], [x, y]) == S.EmptySet

