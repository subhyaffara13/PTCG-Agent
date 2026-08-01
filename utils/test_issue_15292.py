
def test_issue_15292():
    res = integrate(exp(-x**2*cos(2*t)) * cos(x**2*sin(2*t)), (x, 0, oo))
    assert isinstance(res, Piecewise)
    assert gammasimp((res - sqrt(pi)/2 * cos(t)).subs(t, pi/6)) == 0

