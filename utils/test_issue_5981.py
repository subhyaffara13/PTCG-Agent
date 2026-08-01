
def test_issue_5981():
    u = symbols('u')
    assert integrate(1/(u**2 + 1)) == atan(u)

