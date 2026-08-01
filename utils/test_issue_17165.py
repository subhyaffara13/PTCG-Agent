
def test_issue_17165():
    n = symbols("n", integer=True)
    x = symbols('x')
    s = (x*Sum(x**n, (n, -1, oo)))
    ssimp = s.doit().simplify()

    assert ssimp == Piecewise((-1/(x - 1), (x > -1) & (x < 1)),
                              (x*Sum(x**n, (n, -1, oo)), True)), ssimp
    assert ssimp.simplify() == ssimp

