
def test_issue_15509():
    from sympy.vector import CoordSys3D
    N = CoordSys3D('N')
    x = N.x
    assert integrate(cos(a*x + b), (x, x_1, x_2), heurisch=True) == Piecewise(
        (-sin(a*x_1 + b)/a + sin(a*x_2 + b)/a, (a > -oo) & (a < oo) & Ne(a, 0)), \
            (-x_1*cos(b) + x_2*cos(b), True))

