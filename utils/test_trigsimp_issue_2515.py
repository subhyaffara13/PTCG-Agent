
def test_trigsimp_issue_2515():
    x = Symbol('x')
    assert trigsimp(x*cos(x)*tan(x)) == x*sin(x)
    assert trigsimp(-sin(x) + cos(x)*tan(x)) == 0

