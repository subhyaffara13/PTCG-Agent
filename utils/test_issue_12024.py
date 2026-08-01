
def test_issue_12024():
    x, y = symbols('x y')
    assert solve(Piecewise((0.0, x < 0.1), (x, x >= 0.1)) - y) == \
        [{y: Piecewise((0.0, x < 0.1), (x, True))}]

