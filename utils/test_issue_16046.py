
def test_issue_16046():
    assert integrate(exp(exp(I*x)), [x, 0, 2*pi]) == 2*pi

