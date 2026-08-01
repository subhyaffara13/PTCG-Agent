
def test_issue_1888():
    f = Function('f')
    assert integrate(f(x).diff(x)**2, x).has(Integral)

