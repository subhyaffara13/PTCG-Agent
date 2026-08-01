
def test_issue_5948():
    a, x, y = symbols('a x y')
    assert trigsimp(diff(integrate(cos(x)/sin(x)**7, x), x)) == \
           cos(x)/sin(x)**7

