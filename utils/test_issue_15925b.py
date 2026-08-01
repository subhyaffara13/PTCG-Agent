
def test_issue_15925b():
    f = sqrt((-12*cos(x)**2*sin(x))**2+(12*cos(x)*sin(x)**2)**2)
    assert integrate(f, (x, 0, pi/6)) == Rational(3, 2)

