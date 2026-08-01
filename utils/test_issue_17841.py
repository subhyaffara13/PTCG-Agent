
def test_issue_17841():
    f = diff(1/(x**2+x+I), x)
    assert integrate(f, x) == 1/(x**2 + x + I)

