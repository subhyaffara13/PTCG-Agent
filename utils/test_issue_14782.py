
def test_issue_14782():
    f = sqrt(-x**2 + 1)*(-x**2 + x)
    assert integrate(f, [x, -1, 1]) == - pi / 8

