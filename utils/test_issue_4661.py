
def test_issue_4661():
    a, x, y = symbols('a x y')
    eq = -4*sin(x)**4 + 4*cos(x)**4 - 8*cos(x)**2
    assert trigsimp(eq) == -4
    n = sin(x)**6 + 4*sin(x)**4*cos(x)**2 + 5*sin(x)**2*cos(x)**4 + 2*cos(x)**6
    d = -sin(x)**2 - 2*cos(x)**2
    assert simplify(n/d) == -1
    assert trigsimp(-2*cos(x)**2 + cos(x)**4 - sin(x)**4) == -1
    eq = (- sin(x)**3/4)*cos(x) + (cos(x)**3/4)*sin(x) - sin(2*x)*cos(2*x)/8
    assert trigsimp(eq) == 0

