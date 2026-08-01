
def test_issue_11845a():
    assert not integrate(exp(y - x**3), (x, 0, 1)).has(Integral)

