
def test_issue_14782_slow():
    f = sqrt(-x**2 + 1)*(-x**2 + x)
    assert integrate(f, [x, 0, 1]) == S.One / 3 - pi / 16

