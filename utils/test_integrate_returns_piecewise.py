
def test_integrate_returns_piecewise():
    assert integrate(x**y, x) == Piecewise(
        (x**(y + 1)/(y + 1), Ne(y, -1)), (log(x), True))
    assert integrate(x**y, y) == Piecewise(
        (x**y/log(x), Ne(log(x), 0)), (y, True))
    assert integrate(exp(n*x), x) == Piecewise(
        (exp(n*x)/n, Ne(n, 0)), (x, True))
    assert integrate(x*exp(n*x), x) == Piecewise(
        ((n*x - 1)*exp(n*x)/n**2, Ne(n**2, 0)), (x**2/2, True))
    assert integrate(x**(n*y), x) == Piecewise(
        (x**(n*y + 1)/(n*y + 1), Ne(n*y, -1)), (log(x), True))
    assert integrate(x**(n*y), y) == Piecewise(
        (x**(n*y)/(n*log(x)), Ne(n*log(x), 0)), (y, True))
    assert integrate(cos(n*x), x) == Piecewise(
        (sin(n*x)/n, Ne(n, 0)), (x, True))
    assert integrate(cos(n*x)**2, x) == Piecewise(
        ((n*x/2 + sin(n*x)*cos(n*x)/2)/n, Ne(n, 0)), (x, True))
    assert integrate(x*cos(n*x), x) == Piecewise(
        (x*sin(n*x)/n + cos(n*x)/n**2, Ne(n, 0)), (x**2/2, True))
    assert integrate(sin(n*x), x) == Piecewise(
        (-cos(n*x)/n, Ne(n, 0)), (0, True))
    assert integrate(sin(n*x)**2, x) == Piecewise(
        ((n*x/2 - sin(n*x)*cos(n*x)/2)/n, Ne(n, 0)), (0, True))
    assert integrate(x*sin(n*x), x) == Piecewise(
        (-x*cos(n*x)/n + sin(n*x)/n**2, Ne(n, 0)), (0, True))
    assert integrate(exp(x*y), (x, 0, z)) == Piecewise(
        (exp(y*z)/y - 1/y, (y > -oo) & (y < oo) & Ne(y, 0)), (z, True))
    # https://github.com/sympy/sympy/issues/23707
    assert integrate(exp(t)*exp(-t*sqrt(x - y)), t) == Piecewise(
        (-exp(t)/(sqrt(x - y)*exp(t*sqrt(x - y)) - exp(t*sqrt(x - y))),
        Ne(x, y + 1)), (t, True))

