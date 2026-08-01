
def test_issue_4703():
    g = Function('g')
    assert integrate(exp(x)*g(x), x).has(Integral)

