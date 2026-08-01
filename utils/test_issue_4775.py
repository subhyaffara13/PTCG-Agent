
def test_issue_4775():
    a, x, y = symbols('a x y')
    assert trigsimp(sin(x)*cos(y)+cos(x)*sin(y)) == sin(x + y)
    assert trigsimp(sin(x)*cos(y)+cos(x)*sin(y)+3) == sin(x + y) + 3

