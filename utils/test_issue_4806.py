
def test_issue_4806():
    assert integrate(atan(x)**2, (x, -1, 1)).evalf().round(1) == Float(0.5, 1)
    assert atan(0, evaluate=False).n() == 0

