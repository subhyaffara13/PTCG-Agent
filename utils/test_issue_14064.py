
def test_issue_14064():
    assert integrate(1/cosh(x), (x, 0, oo)) == pi/2

