
def test_issue_3532():
    assert integrate(exp(-x), (x, 0, oo)) == 1

