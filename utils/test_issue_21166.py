
def test_issue_21166():
    assert integrate(sin(x/sqrt(abs(x))), (x, -1, 1)) == 0

