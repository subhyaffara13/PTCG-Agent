
def test_issue_4514():
    assert integrate(sin(2*x)/sin(x), x) == 2*sin(x)

