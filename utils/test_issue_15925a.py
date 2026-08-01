
def test_issue_15925a():
    assert not integrate(sqrt((1+sin(x))**2+(cos(x))**2), (x, -pi/2, pi/2)).has(Integral)

