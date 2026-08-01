
def test_issue_11254c():
    assert not integrate(sech(x)**2, (x, 0, 1)).has(Integral)

