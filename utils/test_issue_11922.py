
def test_issue_11922():
    def f(x):
        return Piecewise((0, x < -1), (1 - x**2, x < 1), (0, True))
    autocorr = lambda k: (
        f(x) * f(x + k)).integrate((x, -1, 1))
    assert autocorr(1.9) > 0
    k = symbols('k')
    good_autocorr = lambda k: (
        (1 - x**2) * f(x + k)).integrate((x, -1, 1))
    a = good_autocorr(k)
    assert a.subs(k, 3) == 0
    k = symbols('k', positive=True)
    a = good_autocorr(k)
    assert a.subs(k, 3) == 0
    assert Piecewise((0, x < 1), (10, (x >= 1))
        ).integrate() == Piecewise((0, x < 1), (10*x - 10, True))

