
def test_issue_14645():
    x, y = symbols('x y')
    assert solve([x*y - x - y, x*y - x - y], [x, y]) == [(y/(y - 1), y)]

