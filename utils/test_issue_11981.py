
def test_issue_11981():
    x, y = symbols('x y', commutative=False)
    assert powsimp((x*y)**2 * (y*x)**2) == (x*y)**2 * (y*x)**2

