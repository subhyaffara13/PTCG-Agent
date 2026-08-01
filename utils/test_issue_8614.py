
def test_issue_8614():
    x = Symbol('x')
    t = Symbol('t')
    assert integrate(exp(t)/t, (t, -oo, x)) == Ei(x)
    assert integrate((exp(-x) - exp(-2*x))/x, (x, 0, oo)) == log(2)

