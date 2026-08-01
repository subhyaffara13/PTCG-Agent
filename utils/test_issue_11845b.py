
def test_issue_11845b():
    assert not integrate(exp(-y - x**3), (x, 0, 1)).has(Integral)

