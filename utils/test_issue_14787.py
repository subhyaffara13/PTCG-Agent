
def test_issue_14787():
    x = Symbol('x')
    f = Piecewise((x, x < 1), ((S(58) / 7), True))
    assert str(f.evalf()) == "Piecewise((x, x < 1), (8.28571428571429, True))"

